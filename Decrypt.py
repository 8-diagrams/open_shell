from Crypto.Cipher import AES
from Crypto.Protocol.KDF import scrypt
from Crypto.Random import get_random_bytes
import os

def encrypt_file(file_path, password, output_path):
    # 生成盐
    salt = get_random_bytes(16)

    # 使用Scrypt生成密钥
    key = scrypt(password.encode(), salt, 32, N=2**14, r=8, p=1)

    # 生成随机IV
    iv = get_random_bytes(16)

    # 创建加密器
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)

    # 读取文件并加密
    with open(file_path, 'rb') as f:
        plaintext = f.read()

    ciphertext = cipher.encrypt(plaintext)

    # 将盐，IV和加密内容写入文件
    with open(output_path, 'wb') as f:
        f.write(salt + iv + ciphertext)

def decrypt_file(encrypted_file_path, password, output_path):
    with open(encrypted_file_path, 'rb') as f:
        data = f.read()

    # 提取盐和IV
    salt = data[:16]
    iv = data[16:32]
    ciphertext = data[32:]

    # 重新生成密钥
    key = scrypt(password.encode(), salt, 32, N=2**14, r=8, p=1)

    # 创建解密器
    cipher = AES.new(key, AES.MODE_CFB, iv=iv)

    # 解密数据
    plaintext = cipher.decrypt(ciphertext)

    # 将解密内容写入文件
    with open(output_path, 'wb') as f:
        f.write(plaintext)

def main():
    import sys 
    file_path = sys.argv[1]  # 替换为要加密的文件路径
    
    password = 'your_secure_password'    # 使用一个强密码
    encrypted_file_path = 'encrypted_file.enc'
    decrypted_file_path = 'decrypted_file.txt'

    encrypt_file(file_path, password, encrypted_file_path)
    print(f"File encrypted and saved to {encrypted_file_path}")

    decrypt_file(encrypted_file_path, password, decrypted_file_path)
    print(f"File decrypted and saved to {decrypted_file_path}")

def enc_backup_file(filename, dest):
    pass 

def read_pwdSuff():
    import os
    user_home_directory = os.path.expanduser('~')
    pwdsuff =  os.path.join( f'{user_home_directory}', '.Encyptpy.conf' ) 
    print(f"cf dir {pwdsuff}")
    if not os.path.exists( pwdsuff ) :
        print(f"need {pwdsuff!r} created" )
        return ''        
    if os.path.exists( pwdsuff  ) :
        with open(pwdsuff) as f :
            return f.read().strip()
    return ''

def tmp_filename_path(filename):
    basefn = f'TMP_{ hashlib.md5( filename.encode("utf8") ).hexdigest() }'
    filename_aes = os.path.basename(filename) + ".aes"
    user_home_directory = os.path.expanduser('~')
    fn = os.path.join( user_home_directory , basefn, filename_aes ) 
    return fn , os.path.join( user_home_directory , basefn)

def tmp_dir_path(dirpath):
    basefn = f'TMP_{ hashlib.md5( dirpath.encode("utf8") ).hexdigest() }'
    filename_aes = dirpath 
    user_home_directory = os.path.expanduser('~')
    fn = os.path.join( user_home_directory , basefn, filename_aes ) 
    return fn , os.path.join( user_home_directory , basefn)

def mymkdir(dirpath):
    try:
        os.makedirs(dirpath)
    except Exception as e:
        print(f"exception {e}")
        pass 
def rcv_upload(dirpath, passwd, base_path):
    #base_path 临时目录 对应 dirpath ，源目录
    mymkdir( base_path )
    files = os.listdir( dirpath )
    for file in files:
        
        fullpath = os.path.join( dirpath, file  )
        if os.path.isfile( fullpath ):
            rel_path = os.path.join( base_path, file +'.aes' )
            print(f"{fullpath} => {rel_path}")
            encrypt_file(fullpath, passwd, rel_path)    
        elif os.path.isdir( fullpath ):
            rel_path = os.path.join( base_path, file )
            rcv_upload( fullpath, passwd, rel_path  )
                
     
import hashlib

if __name__ == "__main__":
    import sys 
    
    decrypt_file(sys.argv[1], sys.argv[3], sys.argv[2]  )
        
        
        