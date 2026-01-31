import base64
import hashlib
from datetime import datetime


class Person:
    def __init__(self, data, static_folder, lang="en"):
        self.first_name = data.get('first_name', '')
        self.last_name = data.get('last_name', '')
        self.title = data.get('title', '')
        self.phone = data.get('phone', '')
        self.email = data.get('email', '')
        self.website = data.get('website', '')
        self.linkedin = data.get('linkedin', '')
        self.github = data.get('github', '')
        self.matrix = data.get('matrix', '')

        # Cím felbontása (érdemes a json-ben is így tárolni)
        self.address_street = data.get('address_street', '')
        self.address_city = data.get('address_city', 'Budapest')
        self.address_zip = data.get('address_zip', '')
        self.address_country = data.get('address_country', 'Hungary')

        self.profile_image = data.get('profile_image', '')
        self.static_folder = static_folder
        self.birth_date = data.get('birth_date', '')

        self.lang = lang

    @property
    def full_name(self):
        if self.lang == "hu":
            return f"{self.last_name} {self.first_name}"
        return f"{self.first_name} {self.last_name}"

    @property
    def address(self):
        if not self.address_country:
            return ""
        if not self.address_city:
            return self.address_country
        if not self.address_zip:
            return f"{self.address_country}, {self.address_city}"
        if not self.address_street:
            return f"{self.address_country}, {self.address_city} {self.address_city}"
        return f"{self.address_country}, {self.address_city} {self.address_city} {self.address_street}"


    def get_photo_b64(self):
        import os
        img_path = os.path.join(self.static_folder, self.profile_image)
        if os.path.exists(img_path):
            with open(img_path, "rb") as img_f:
                return base64.b64encode(img_f.read()).decode('utf-8')
        return ""

    def generate_vcard(self):
        email_hash = hashlib.md5(self.email.encode()).hexdigest()
        uid = f"nurefexc-dev-{email_hash}"
        rev = datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')
        photo = self.get_photo_b64()

        vcard = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"FN:{self.last_name} {self.first_name}",
            f"N:{self.last_name};{self.first_name};;;",
            "NICKNAME:nurefexc",
            "ORG:Nurefexc Solutions",
            f"TITLE:{self.title}",
            f"TEL;TYPE=CELL:{self.phone}",
            f"EMAIL;TYPE=WORK,INTERNET:{self.email}",
            f"URL;TYPE=WORK:https://{self.website}",
            # Cím formátum: PO Box; Extended; Street; City; Region; Zip; Country
            f"X-SOCIALPROFILE;TYPE=linkedin:{self.linkedin}",
            f"X-SOCIALPROFILE;TYPE=github:{self.github}",
            f"IMPP;PREF:matrix:https://matrix.to/#/{self.matrix}",
            f"REV:{rev}",
            f"UID:{uid}"
        ]

        if photo:
            vcard.append(f"PHOTO;TYPE=PNG;ENCODING=b:{photo}")

        vcard.append("END:VCARD")
        return "\r\n".join(vcard)