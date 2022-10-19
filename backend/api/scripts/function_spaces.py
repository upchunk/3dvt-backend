from boto3.session import Session

SPACE_NAME = "3dvt-space"

session = Session()
client = session.client(
    "s3",
    region_name="sgp1",
    endpoint_url="https://sgp1.digitaloceanspaces.com",
    aws_access_key_id="DO00UU7PG2P7BFLZ6QEB",  # Access Key ID
    aws_secret_access_key="OLz7rFWgLdQtR5qjsuqD6hpEdUOnbm5U6WaPYcsMBb4",
)  # Secret Access Key

# Parameter
# path_to_file = Path menuju ke file yang ingin diupload
# key_file = Nama yang ingin digunakan saat disimpan di Space


def upload_file(path_to_file, key_file):
    client.upload_file(path_to_file, SPACE_NAME, key_file)


# Parameter
# file_in_space = Path menuju ke file yang ingin didownload di Space
# file_path = Nama yang ingin digunakan saat disimpan di lokal


def download_file(file_in_space, file_path):
    client.download_file(SPACE_NAME, file_in_space, file_path)


# Parameter
# file_in_space = Path menuju ke file yang ingin dihapus di Space


def delete_file(file_in_space):
    client.delete_object(Bucket=SPACE_NAME, Key=file_in_space)
