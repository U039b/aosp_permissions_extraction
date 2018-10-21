# AOSP permissions extraction toy
This toy tool is meant to extract:
* permission groups (name, icon, label, description)
* permissions (name, label, description, group, protection level)

from the AOSP sources and generate a JSON file containing information listed above in the locale you choose. 

This tool uses the [VectorDrawable2Svg script of Alessandro Lucchet](https://gitlab.com/Hyperion777/VectorDrawable2Svg) which has been lightly modified.

**This toy is only compatible with Python 3.x**

## Preliminaries
First of all, you have to clone the huge AOSP repository and optionnaly remove useless content:
```
mkdir AOSP
git clone https://github.com/aosp-mirror/platform_frameworks_base.git AOSP
cd AOSP
rm -rf  Android.bp Android.mk apct-tests api CleanSpec.mk cmds config data docs drm graphics keystore libs location lowpan media MODULE_LICENSE_APACHE2 native nfc-extras NOTICE obex opengl packages pathmap.mk PREUPLOAD.cfg proto rs samples sax services startop telecomm telephony test-base test-legacy test-mock test-runner tests tools vr wifi
```

## Usage
```
python extract.py [path to AOSP folder] [2-letter locale] [destination folder]
```
the destination folder will be automatically created.

## Example of outputs
The `dist` folder versioned in this repository gives you an example of output in various locales.
```
dist
  ├── permissions-en.html
  ├── permissions-en.json
  ├── permissions-es.html
  ├── permissions-es.json
  ├── permissions-fr.html
  ├── permissions-fr.json
  ├── permissions-it.html
  ├── permissions-it.json
  ├── permissions-ja.html
  └── permissions-ja.json
```