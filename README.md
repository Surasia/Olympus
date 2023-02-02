# Olympus

## Credits

This plugin is based on [HIME](https://github.com/MontagueM/HaloInfiniteModelExtractor) by MontagueM.  
Module support is based on [HIMU](https://github.com/MontagueM/HaloInfiniteModuleUnpacker) by MontagueM and parts of [Adjutant](https://github.com/Gravemind2401/Adjutant).  
Research and Code for BSPs: [PlasteredCrab](https://github.com/PlasteredCrab)  
[HaloInfiniteTagEditor](https://github.com/Z-15/Halo-Infinite-Tag-Editor) by Z-15, very useful for research  
[IRTV](https://github.com/Gamergotten/Infinite-runtime-tagviewer), tag definitions
[HaloInfiniteResearch](https://github.com/urium1186/HaloInfiniteResearch/tree/develop) for coating importing.

## General
### Initial Set-Up
Set the "Asset Root" in addon preferences to your Halo Infinite unpack folder. Make sure to use forward slashes (/) and have the path end with it too.
### Models
To import models, make sure all related chunk files are in the same folder and import the .render_model file. 

## Installing texture2ddecoder/pymmh3
To install python modules for blender, they have to be installed into blenders python environment, not the system environment. To do this, go to the python console in blender (for example in the scripting workspace) and enter
```
import ensurepip
ensurepip.bootstrap()
```
to install pip into blenders python environment. Then enter
```
import pip
pip.main(['install','texture2ddecoder'])
pip.main(['install','pymmh3'])
```
to install the modules. Pip might complain that a newer version of pip is available, but that can just be ignored.
