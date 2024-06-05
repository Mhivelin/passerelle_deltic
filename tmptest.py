import socket

# Obtenir le nom de l'hôte
hostname = socket.gethostname()

# Obtenir l'adresse IP de l'hôte
ip_address = socket.gethostbyname(hostname)

print(f"Nom de l'hôte : {hostname}")
print(f"Adresse IP de l'hôte : {ip_address}")
