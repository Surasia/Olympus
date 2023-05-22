# Olympus

# Credits

This plugin is based on [HIME](https://github.com/MontagueM/HaloInfiniteModelExtractor) by MontagueM.  
Module support is based on [HIMU](https://github.com/MontagueM/HaloInfiniteModuleUnpacker) by MontagueM and parts of [Adjutant](https://github.com/Gravemind2401/Adjutant).  
Research and Code for BSPs: [PlasteredCrab](https://github.com/PlasteredCrab)  
[HaloInfiniteTagEditor](https://github.com/Z-15/Halo-Infinite-Tag-Editor) by Z-15, very useful for research  
[HIMS](https://github.com/AverageTrapEnthusiast/Halo-Infinite-Shader-Resources) by AGE and ChromaCore

## Initial Set-Up
- Download [InfiniteExplorer](https://github.com/Coreforge/infiniteExplorer) with Fuse
- Install [WinFSP](https://winfsp.dev/rel/)
- Load all modules in Halo Infinite's deploy folder in InfiniteExplorer, and mount to `M:`
- Download Olympus and install it as a Blender addon.
- In addon settings, set "Asset Root" to `M:/`

## Installing Required modules
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


## Importing .materialstyles
- To import materialstyles (aka coatings), navigate to the same folder in where you found your render model.
- MaterialStyle files can be found in a subfolder called "coatings" or "styles"
  - Ex:  `M:\__chore\gen__\objects\characters\brute\styles`
