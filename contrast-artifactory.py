#!/usr/bin/env python3
import requests
import zipfile
import re
import os
import json

authorization="change-me"
apikey="change-me"
artifactory_auth="change-me"
artifactory_url="change-me"
orgid="change-me"
contrast_url = "https://app.contrastsecurity.com/Contrast/api/ng/" + orgid + "/agents/default/JAVA"
jarfile="contrast.jar"
artifactory_payload = {}
artifactory_headers= {
  'Authorization': artifactory_auth,
  'Content-Type': 'application/java-archive'
}
contrast_payload = {}
contrast_headers = {
  'Authorization': authorization,
  'API-Key': apikey,
  'Accept': 'application/json',
}

def main():
  cleanup()

  contrast_response = requests.request("GET", contrast_url, headers=contrast_headers, data = contrast_payload)
  
  with open('contrast.jar', 'wb') as f:
    f.write(contrast_response.content)
  
  versionfinder()
  artifactory_check()
  artifactory_push()

  cleanup()

def versionfinder():
  if zipfile.is_zipfile(jarfile):
    print(f'{jarfile} is a valid zip file')
  else:
    raise Exception(f'{jarfile} is a not a valid zip file')
  
  zfile = zipfile.ZipFile( jarfile, "r" )
  print('-'*40)

  filename="META-INF/MANIFEST.MF"

  with zfile as z:
    with z.open(filename) as f:
        for line in f:
            if "Implementation-Build" in line.decode():
              global contrast_version
              contrast_version=line.decode().split(":")[1]
              print(f'Contrast is version: {contrast_version}')

def artifactory_check():
  try:
    r = requests.head(artifactory_url + contrast_version, allow_redirects=True)
    print(r.status_code)
    if r.status_code == 200:
      raise Exception('This version is already in Artifactory')
    else:
      print('This version is not yet in Artifactory')

  except requests.ConnectionError:
    print("failed to connect")

def artifactory_push():
  try:
    artifactory_push_url=artifactory_url + contrast_version.strip() + "/contrast.jar"
    artifactory_push_url_latest=artifactory_url + "latest/contrast.jar"

    print("Pushing contrast.jar to: " + artifactory_push_url)
    artifactory_response = requests.request("PUT", artifactory_push_url, headers=artifactory_headers, data = open(jarfile, 'rb'))
    pretty_artifactory_response = json.loads(artifactory_response.text)
    print(json.dumps(pretty_artifactory_response, indent=2))

    print("Now pushing contrast.jar file to 'latest' path: " + artifactory_push_url_latest)
    artifactory_latest_response = requests.request("PUT", artifactory_push_url_latest, headers=artifactory_headers, data = open(jarfile, 'rb'))
    pretty_artifactory_latest_response = json.loads(artifactory_latest_response.text)
    print(json.dumps(pretty_artifactory_latest_response, indent=2))

  except requests.ConnectionError:
    print("failed to connect")

def cleanup():
  if os.path.exists(jarfile):
    os.remove(jarfile)
    print("Deleted previous contrast.jar file")
  else:
    print("Contrast.jar not present, no need to delete")

  

if __name__ == '__main__':
  main()
