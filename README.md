# Olympus

# Credits

This plugin is based on [HIME](https://github.com/MontagueM/HaloInfiniteModelExtractor) by MontagueM.  
Module support is based on [HIMU](https://github.com/MontagueM/HaloInfiniteModuleUnpacker) by MontagueM and parts of [Adjutant](https://github.com/Gravemind2401/Adjutant).  
Research and Code for BSPs: [PlasteredCrab](https://github.com/PlasteredCrab)  
[HaloInfiniteTagEditor](https://github.com/Z-15/Halo-Infinite-Tag-Editor) by Z-15, very useful for research  
[IRTV](https://github.com/Gamergotten/Infinite-runtime-tagviewer), tag definitions
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

## Importing render_models
- To import models, navigate to the `M:\__chore\gen__` folder. This is usually where models are found, but there are some exceptions to this such as spartan_armor.
- Navigate to the specific model that you want to import.
- Select the render_model tag and import with the following options enabled:
  - Import UVs
  - Import Materials
  - Import Mesh

![select model](https://user-images.githubusercontent.com/74399067/219308314-8b472490-8726-4cd0-ab1a-5c5bfcb8f7b4.gif)


## Importing .materialstyles
- To import materialstyles (aka coatings), navigate to the same folder in where you found your render model.
- MaterialStyle files can be found in a subfolder called "coatings" or "styles"
  - Ex:  `M:\__chore\gen__\objects\characters\brute\styles`
- Click on a materialstyle tag and wait for coatings to load.
- Select a specific coating you want to import.

![select coating](https://user-images.githubusercontent.com/74399067/219304810-844475df-74b7-42e9-a5a1-add8c22f23d6.gif)

- For import options, set options for;

  - `Material Path:` path where your .material tags are found. This is usually outside of `__chore\gen__`, being in the regular directory of your file. 
      - Ex: `M:\objects\characters\spartan_armor\materials`

  - `Selected Objects Only` is exactly what it is says. Make sure to have at least one "active" object selected (aka light orange outlined object)
  
  - `Weighted Normals/Clean Up` attemps to correct/guess mesh normals based on face data, and remove LODs. Recommended for Infinite's models.
  
  - `Purge Orphans` recursively removes unused data after every material import. Useful for models that use hundreds of materials, like the Pelican.
  
  - `Cross Core` disables the requirement for materialstyles to match materials. Useful for importing coatings that aren't available on a specific model.
  
  - `Zone 7 (Damage)` enables the 7th zone in models, which is usually used to add additional detail to models. This remains unused on models such as multiplayer armor.
  
  - `Move UVs` moves UVs up by the amount selected in the slider. This is to ensure proper scaling, and the default correction amount is 1. This only needs to be done on one import.

- Import your materialstyle.

