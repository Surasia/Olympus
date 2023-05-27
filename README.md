# Olympus

# Credits

- This plugin is based on [HIME](https://github.com/MontagueM/HaloInfiniteModelExtractor) by MontagueM
- Module support is based on [HIMU](https://github.com/MontagueM/HaloInfiniteModuleUnpacker) by MontagueM and parts of [Adjutant](https://github.com/Gravemind2401/Adjutant).  
- Research and Code for BSPs: [PlasteredCrab](https://github.com/PlasteredCrab)  
- Shader: [HIMS](https://github.com/AverageTrapEnthusiast/Halo-Infinite-Shader-Resources) by AGE and ChromaCore
- Materials and the basis of the plugin: [HIRT](https://github.com/urium1186/HIRT) by Urium86


# Setting up

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

## Installation
- Install [WinFSP](https://winfsp.dev/rel/)
- Download [InfiniteExplorer](https://github.com/Coreforge/infiniteExplorer#nightly) with FUSE, and make sure to use the Nightly build, and follow the instructions provided.
- Load all modules in Halo Infinite's deploy folder in InfiniteExplorer, and mount to `M:`
- Download Olympus and install it as a Blender addon.
- In addon settings, set "Asset Root" to `M:/`

## Setting up the addon
After you've done with the installation and prerequisites, you can now navigate to the Blender Addon settings. Make sure to set your asset path to `M:/`.

![](https://github.com/Surasia/Olympus/assets/74399067/9b547d32-2895-4f67-9ac4-36ab8b7cae3c)

## Downloading Coatings and Materials
- Coatings use special JSON files which can be found in [My Olympus Coatings repository](https://github.com/Surasia/OlympusCoatings). The files are named appropriately, and can be stored anywhere.
- Materials also require a download, available in this [link](https://mega.nz/file/8uBBWLjD#hR561kILaWgHCsENda5Dtvqis_pRPE9x63oUEiPSfeA). Unzip and place this anywhere you want, and this will be your "material path" in the coming sections.

# Usage

## Outline

**IMPORTANT: Old ports past Season 3 will not work with this.**
For the main purpose of this tool, you can navigate to the "Import" menu, where you will find "Import Halo Infinite Coating". This is where we will want to navigate to our coatings folder, which we downloaded [here.](https://github.com/Surasia/Olympus/edit/develop/README.md#downloading-coatings-and-materials)

![](https://github.com/Surasia/Olympus/assets/74399067/a2acfceb-6517-4982-ad9e-1925f4b8cca5)

## Import Settings
  
  - `Material Path:` where you downloaded the material zip. Make sure to use backwards slashes.

  - `Selected Objects Only` is exactly what it is says. Make sure to have at least one "active" object selected (aka light orange outlined object)
  
  - `Weighted Normals/Clean Up` attemps to correct/guess mesh normals based on face data, and merges vertices. Recommended for Infinite's models.
  
  - `Move UVs` moves UVs up by the amount selected in the slider. This is to ensure proper scaling, and the default correction amount is 1. This only needs to be done on one import.
 
  - `Cross Core` disables the requirement for materialstyles to match materials. Useful for importing coatings that aren't available on a specific model.
  
  - `Zone 7 (Damage)` enables the 7th zone in models, which is usually used to add additional detail to models. This remains unused on models such as multiplayer armor.

  - `Purge Orphans` recursively removes unused data after every material import. Useful for models that use hundreds of materials, like the Pelican.

Now press "Import", and your coating should import. Have fun!
