import argparse
import socket
import random
import time
from urllib.parse import urlparse
from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr1, send
from scapy.all import sniff, wrpcap, rdpcap

def resolve_hostname(hostname):
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        return None

def parse_url(url_arg):
    if not url_arg.startswith(('http://', 'https://')):
        url_arg = 'http://' + url_arg
    try:
        parsed = urlparse(url_arg)
        return parsed.hostname, (parsed.path or '/'), parsed.scheme
    except:
        return None, None, None

def send_http_request(hostname, path, custom_request=None):
    dest_ip = resolve_hostname(hostname)
    if not dest_ip: return None
    port, client_sport = 80, random.randint(1025, 65500)
    http_request_str = custom_request or f'GET {path} HTTP/1.1\r\nHost: {hostname}\r\nConnection: close\r\n\r\n'
    
    syn = IP(dst=dest_ip) / TCP(sport=client_sport, dport=port, flags='S')
    syn_ack = sr1(syn, timeout=2, verbose=False)
    if not syn_ack or syn_ack[TCP].flags != 0x12: return None
    
    send(IP(dst=dest_ip) / TCP(sport=client_sport, dport=port, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='A'), verbose=False)
    send(IP(dst=dest_ip) / TCP(sport=client_sport, dport=port, seq=syn_ack[TCP].ack, ack=syn_ack[TCP].seq + 1, flags='PA') / http_request_str, verbose=False)
    return dest_ip

def capture_traffic(hostname, timeout=30, output_file=None):
    dest_ip = resolve_hostname(hostname)
    print(f"Сбор трафика для {hostname}...")
    packets = sniff(iface='en0', filter=f"tcp port 80", timeout=timeout)
    if output_file and packets:
        wrpcap(output_file, packets)
    return packets

def analyze_packets(packets):
    if not packets: return print("Трафик пуст")
    for i, pkt in enumerate(packets):
        if pkt.haslayer('Raw'):
            data = pkt['Raw'].load.decode('utf-8', errors='ignore')
            if any(p in data.lower() for p in ['<script>', 'alert(', 'onerror=']):
                print(f"[!] XSS обнаружена в пакете {i}:\n{data[:200]}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--send')
    parser.add_argument('--capture')
    parser.add_argument('--analyze')
    parser.add_argument('--timeout', type=int, default=30)
    parser.add_argument('--output')
    parser.add_argument('--request')
    args = parser.parse_args()

    if args.capture:
        analyze_packets(capture_traffic(args.capture, args.timeout, args.output))
    if args.analyze:
        analyze_packets(rdpcap(args.analyze))
    if args.send:
        h, p, _ = parse_url(args.send)
        send_http_request(h, p, args.request)

if __name__ == '__main__':
    main()
