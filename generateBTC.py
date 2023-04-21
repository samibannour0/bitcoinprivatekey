import hashlib
import ecdsa
import requests
import random
start_range = 0x20000000000000000
end_range = 0x3ffffffffffffffff
address = '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so'

for i in range(start_range, end_range):
    # Convert the integer to a 32-byte hex string
    private_key_hex = hex(i)[2:].zfill(64)
    # Convert the hex string to bytes
    private_key_bytes = bytes.fromhex(private_key_hex)

    # Generate the public key from the private key
    signing_key = ecdsa.SigningKey.from_string(private_key_bytes, curve=ecdsa.SECP256k1)
    verifying_key = signing_key.get_verifying_key()
    public_key_bytes = verifying_key.to_string()

    # Calculate the public key hash
    public_key_hash_bytes = hashlib.new('ripemd160', hashlib.sha256(public_key_bytes).digest()).digest()

    # Encode the public key hash to an address
    alphabet = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
    def base58_encode(bytes_input):
        base_count = len(alphabet)
        result = ''
        num = int.from_bytes(bytes_input, byteorder='big')
        while num > 0:
            num, mod = divmod(num, base_count)
            result = alphabet[mod] + result
        return result
    new_address = base58_encode(b'\x00' + public_key_hash_bytes)

    if new_address == address:
        print(f"Private key: {private_key_hex}")
        print(f"Public key: {public_key_bytes.hex()}")
        print(f"Address: {new_address}")
        print(f"Balance: Checking...")

        # Check the balance of the address
        try:
            response = requests.get(f"https://blockchain.info/q/addressbalance/{address}")
            balance = int(response.text)
            print(f"Balance: {balance}")
            break
        except:
            print("Error checking balance.")
            break

    else:
        print(f"Private key: {private_key_hex}")
        print(f"Public key: {public_key_bytes.hex()}")
        print(f"Address: {new_address}")
        print(f"Balance: 0")
