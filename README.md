# wolfdotsolar
Solar Observation Processing Pipeline

## 1. Build Docker Image
```
./Docker/buildDockerImage.sh
```

## 2. Launch Crop & Stack Pipeline
```
docker run  --rm -v /folder/with/sun/pictures/:/imgs isontheline/wolfdotsolar:latest cropnstack "/imgs/*.JPG"
```

## 3. Example Result
![Sun Cropped and Stacked with wolfdotsolar](/samples/sun-cropped-and-stacked-with-wolfdotsolar.jpg)