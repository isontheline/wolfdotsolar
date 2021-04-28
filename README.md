# wolfdotsolar
Helpers to improve Solar Observation Processing Pipeline

## Build
./Docker/buildDockerImage.sh

## Crop Sun Pictures
```
docker run --rm -v /folder/with/sun/pictures/:/imgs isontheline/wolfdotsolar:latest python3 /opt/wolfdotsolar/crop_sun.py /imgs/*.JPG
```

## Stack Sun Pictures
```
docker run --rm -v /folder/with/sun/pictures/wolfdotsolar/crop/:/imgs/ isontheline/wolfdotsolar:latest PlanetarySystemStacker /imgs/ --stack_percent=50
```

## Unsharp Sun Pictures
```
docker run --rm -v /folder/with/sun/pictures/wolfdotsolar/crop/:/imgs isontheline/wolfdotsolar:latest python3 /opt/wolfdotsolar/unsharp.py /imgs/_pss.png --amount=3 --sigma=3 --radius=100
```

## Exxample Result
![Sun Cropped and Stacked with wolfdotsolar](/samples/sun-cropped-and-stacked-with-wolfdotsolar.jpg)