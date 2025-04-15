from gns3fy import Gns3Connector

BASE_IP = "http://10.48.229."
GNS3_USER = "gns3"
GNS3_PW = "gns3"


# Read last octets from datastore
try:
    with open("last_octet", "r") as f:
        content = f.read()
        SERVER_LAST_OCTETS = [int(num) for num in re.findall(r'\d+', content)]
except Exception as e:
    print("Error reading last_octet file:", e)
    SERVER_LAST_OCTETS = []

if not SERVER_LAST_OCTETS:
    raise ValueError("No valid server last octets found in 'datastore'.")

SERVER_URLS = [f"{BASE_IP}{octet}:80" for octet in SERVER_LAST_OCTETS]

# Connect and delete all projects from each server
for SERVER_URL in SERVER_URLS:
    try:
        server = Gns3Connector(url=SERVER_URL, user=GNS3_USER, cred=GNS3_PW)
        version = server.get_version()
        print(f"\nConnected to GNS3 server {SERVER_URL} (version: {version})")

        projects = server.get_projects() #print out all projects existing in the machine
        if not projects:
            print("  No projects to delete.")
        else:
            try:
                with open ("projects_to_delete.txt", "r") as f:
                    PROJECTS_TO_DELETE = [line.strip() for line in f if line.strip()]
            except Exception as e:
                print ("Error reading 'Projects_to_delete.txt' file: ", e)
                PROJECTS_TO_DELETE = []
            if not PROJECTS_TO_DELETE:
                raise ValueError("No valid project names found in 'projects_to_delete.txt.'.")
        for project in projects:
            if project["name"] in PROJECTS_TO_DELETE:
                try:
                    print(f"Deleting project '{project['name']}'...")
                    server.delete_project(project_id=project["project_id"])
                    print(f"Project '{project['name']}' deleted successfully!")
                except Exception as e:
                    print(f"Failed to delete project '{project['name']}': {e}")


    except Exception as e:
        print(f"Failed to process {SERVER_URL}: {e}")
