# TYPETR-Assistants

This is our new Assistant Tools environment.
All sources for the BaseAssistant classes and additional functions will be kept here, instead of having them copied inside project repositories.

It is a fast and flexible collection of helpers for specific type projects: this repository contains library of assistants and helper for type project.

This collection of tools offers a fast and flexible collection of helpers and assistant examples for specific type projects.

Documentation is at docs/. There may be a website later.

## Github

https://github.com/petrvanblokland/TYPETR-Assistants

## Environment

TYPETR-Assistants is developed for RoboFont only.

## Installing

Install for your own use with pip (@@@ Does not work yet):

    $ pip install typetr_assistants
    
Or install from a cloned repository in your local Python version by (@@@ Does not work yet)

	$ python setup.py install

## Naming

### Helpers

In the context of this repository, “Helpers” are scripts that can be run without any coding. They are generic tools that perform a specifc task, such as the editing of curves or building PDF proofs. “Helpers can best be compared with existing tools that live inside the RoboFont extension menu, maintained by Mechanic.

Current operational helpers are:

* CurvePalette.py (see docs/CurvePalette.md)
* GlyphBrowser

### Assistants

“Assistants” are applications that are written for a specific project. They inherit from BaseAssistant classes that take can of the base level of “event” plumbing between tools, UFO’s and RoboFont. Assistant may contain very specific information about the type project, such as glyphset, design space, shape of serifs, position of guide lines and spacing dependencies. Assistant code is likely to live inside the directories of type projects.

## Documentation

All markdown documents (“.md” extension) in this repository can best be opened with MacDown https://macdown.uranusjr.com

## Usage

* Some generic helpers (scripts with a specific task, such as the CurvePalette and the GlyphBrowser) will be supplied in this repository, ready to use without any coding. Note that these are ”simple” scripts that will develop overtime, without specific knowledge about a particular design project.
* Helper names carry a version number. While developing them further, we’ll some older versions available. “beta” is the latest, adding functions but use it with care. It is safer to use one of the older versions.
* The TYPETR-Assistant assistantLib/ library exists as a set of evolving base classes that can be used to create your own local Project Assistants. It is supplied as a toolkit without warrenty or support.  
* We’ll try to keep everything backward compatible as much as we can, but there is no guarantee that this will always be possible.
* Since TYPETR-Assistants are published as open source under MIT licensing, written from scratch without the inclusion of proprietary code, you are free to use all tools for your own projects as much as you like.

## Dependencies

TYPETR-Assistants imports open source type libraries, such as:

* vanilla/ (by Tal Leming)
* fontmake/ (by Google and Just van Rossum)
* drawBot/ (by Frederik Berlaen and Just van Rossum)
* merz/ and ezui/ (by Tal Leming) 

Special thanks to all designers, coders and companies who published the sources that TYPETR-Assistants are based on.

## Contributions

Any contribution, reporting code issues or extending documentation is appreciated.

## Tool wishes

* the “g” key function to place the points at the same place
* bis - with the option of placing the glyph on the left, in the middle or on the right.
* the text sample in FontGoggles.
* save all (and close all).
* color marker on the glyphs you just did
* preview left and right
* I would also add an option of copying spacing from one glyph to another and auto adjusting it, that’s one of my fav things!
* For TYPETR-Polator: Side by side glyph comparison and font preview like in prepolator.

## TYPETR and TYPE-TRY are registered trademarks by Buro Petr van Blokland + Claudia Mens