import bcrypt
import yaml

passwords = ['12345', '67890']


def hash_passwords(passwords):
    hashed_passwords = []
    for password in passwords:
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        hashed_passwords.append(hashed.decode())
    return hashed_passwords


hashed_passwords = hash_passwords(passwords)

user_config = {
    'credentials': {
        'usernames': {
            'user1': {
                'email': 'tiktok@techjam.com',
                'name': 'TikTokTechJam',
                'password': hashed_passwords[0]
            },
            'user2': {
                'email': 'clock@gmail.com',
                'name': 'CLOCK',
                'password': hashed_passwords[1]
            }
        }
    },
    'cookie': {
        'expiry_days': 30,
        'key': 'AT8YNW9uTr6ApPkmB8k5dGx09zSOVmhl',
        'name': 'TikTokTechJam-CLOCK',
    },
    'preauthorized': {
        'emails': [
            'hehe@gmail.com'
        ]
    },
}

with open('config.yaml', 'w') as file:
    yaml.dump(user_config, file)
