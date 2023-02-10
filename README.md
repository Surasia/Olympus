# blender-halo-infinite

# Credits

This plugin is based on [HIME](https://github.com/MontagueM/HaloInfiniteModelExtractor) by MontagueM.  
Module support is based on [HIMU](https://github.com/MontagueM/HaloInfiniteModuleUnpacker) by MontagueM and parts of [Adjutant](https://github.com/Gravemind2401/Adjutant).  
Research and Code for BSPs: [PlasteredCrab](https://github.com/PlasteredCrab)  
[HaloInfiniteTagEditor](https://github.com/Z-15/Halo-Infinite-Tag-Editor) by Z-15, very useful for research  
[IRTV](https://github.com/Gamergotten/Infinite-runtime-tagviewer), tag definitions

# General
To import models, make sure all related chunk files are in the same folder and import the .render_model file. 
Importing Textures requires the module texture2ddecoder to be installed for blender.

# Shaders
To automatically apply the textures to the models, the shader needs to have Image Texture nodes named "normal", "asg", "mask_0" and "mask_1", corresponding to the textures. If there are issues with shaders not getting copied properly (the position of nodes currently doesn't work, but that's not a functional thing), please open an issue.

# Installing texture2ddecoder
## All platforms
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
to install the module texture2ddecoder. Pip might complain that a newer version of pip is available, but that can just be ignored.
