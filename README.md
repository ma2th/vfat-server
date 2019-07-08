# Visual Field Assessment and Training (VFAT): Server for Mobile and Home Perimetry

## Features 
- Perform continuous home monitoring of your visual field
- Measure equidistantly-sampled visual fields or Octopus G1-based visual fields
- Online storage and evaluation of results
- Use perceptual learning to improve (or even recover) your visual field 
- Implemented using Unreal Engine 4 (UE4) and Google VR to facilitate exporting the app for all major smartphone operating systems
- See also [vfat.mad.tf.fau.de](https://www.vfat.mad.tf.fau.de/home/)

## Requirements
- Smartphone
- Virtual reality (VR) headset
- Bluetooth input device
- [VFAT smartphone app](https://github.com/ma2th/vfat-app)

## Configuration ([Django](https://www.djangoproject.com/) related)
1. Create file non-opensource/config/media_root.txt and enter the full path of the media root directory for the production environment
2. Create file non-opensource/config/static_root.txt and enter the full path of the static root directory for the production environment
3. Create file non-opensource/config/secret_key.txt and enter the secret key

## Important Scripts
- run.sh runs the server with the local debug environment
- reset.sh resets the server
- python manage.py runserver runs the server with the production environment

