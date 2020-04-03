# PrediChord
> Here goes your awesome project description!

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Examples of use](#examples-of-use)
* [Project status](#project-status)

## General info
Motivation: To have automatically created chord sequences based on our listening preferences. To help with the process of creating new music. Have the chord sequences played back to me. Jam on the violin. 

Uses techniques from the fields of data retrieval and natural language processing, offers many music-related functionalities. 

To this end, we designed the following functionalities to work in the following specific order. However, most functionalities can be used standalone, if so desired. See (#features).

- Uses your very Spotify streaming data of last 90 days (Ask spotify, link), or mine ([@Evadeschipper]), if you're just trying it out. 
- Finds the chords for the songs you've listened to on ultimate-guitar.com. 
- Trains an n-gram model based on the chord sequences in the songs from your data. 

## Technologies

* Python 3.7

## Setup

Input data - what files and where? Spotify gives you a .zip with files. Extract into cloned repository. You should end up with a folder called 'MyData', in which is your streaming data
How to run
Requirements.txt
Chromedriver is looked for in repository folder. 

## Features

* Transpose a note or chord using any (positive or negative) interval.
* Find the notes belonging to many commonly used chords. 
* Write a midi file playing any given sequence of (commonly used) chords back to you.
* Find the equivalent sounding sharp chord for a chord with a flat root.
* Scrape chords from an ultimate-guitar.com webpage. 
* Find the (likeliest) best version of the chords of a song on ultimate-guitar.com.
* Train a bi- or trigram model, and use it to generate a chord based on the input chord(s) you choose.

The repository also includes a table of the frequencies and wavelengths belonging to the pitches C0 up to and including B8. 

To-do list:
* Implement weighting mechanisms for the chords (such as TD-IDF). 
* Implement other commonly used prediction models. 

## Examples of use

Show examples of usage:
`put-your-code-here`

## Project status

In development.

## Contact
Created by [Eva de Schipper](https://github.com/Evadeschipper) & [Janne Holopainen](https://github.com/Manezki).

