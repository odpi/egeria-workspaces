import http.client
import json
import sys

def delete_resource(conn, method, path):
    try:
        conn.request(method, path, headers={"Content-Type": "application/json"})
        response = conn.getresponse()
        data = response.read().decode()
        print(f"DELETE {path}")
        print(f"Response: {response.status} {response.reason}")
        if data:
            print(f"Body: {data}")
        print("-" * 40)
    except Exception as e:
        print(f"Error deleting {path}: {e}")

def main():
    host = "localhost"
    port = 8087
    base_path = "/api/2.1/unity-catalog"
    
    resources_to_delete = [
        # Volumes
        f"{base_path}/volumes/clinical_trials.werewolf_transformation.weekly_measurements",
        f"{base_path}/volumes/clinical_trials.dragon_breath.weekly_measurements",
        f"{base_path}/volumes/clinical_trials.falcon_feather_mite.weekly_measurements",
        f"{base_path}/volumes/clinical_trials.teddy_bear_drop_foot.weekly_measurements",
        # Schemas
        f"{base_path}/schemas/clinical_trials.teddy_bear_drop_foot"
    ]

    print(f"Connecting to Unity Catalog at {host}:{port}...")
    conn = http.client.HTTPConnection(host, port)
    
    for resource in resources_to_delete:
        delete_resource(conn, "DELETE", resource)
        
    conn.close()
    print("Reset process completed.")

if __name__ == "__main__":
    main()
