# PrediChord
> PrediChord aims to encourage your musical creativity by generating chord sequences based on your listening preferences on Spotify.

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Setup](#setup)
* [Features](#features)
* [Examples of use](#examples-of-use)
* [Project status](#project-status)

## General info
Predichord was created to help with the process of creating new music. We hope that, by having the computer generate chord sequences based on your musical interests and by playing them back to you, your creativity will get sparked. 

The project uses techniques from the fields of data retrieval and natural language processing, and also offers many music-related functionalities. We designed the functionalities to work in the following specific order. However, most functionalities can be used standalone, if so desired. See (#features).

1. Uses your very Spotify streaming data of last 90 days ([ask spotify for your data here](https://www.spotify.com/ca-en/account/privacy/)), or use mine ([Eva de Schipper](https://github.com/Evadeschipper)) if you're just trying it out. 
2. Finds the chords for the songs you've listened to on ultimate-guitar.com. 
3. Trains an n-gram model based on the chord sequences in the songs from your data. 
4. Generates sequences of chords in a stochastic way given a starting chord. 

## Technologies

* Python 3.7

## Setup

To run the code using [your own Spotify data](https://www.spotify.com/ca-en/account/privacy/), extract the .zip file into the PrediChord folder on your computer. You should end up with a folder called `MyData`, which contains (among other things) your streaming data.

Furthermore, you will need a [chromedriver](https://chromedriver.chromium.org/). Put the program file (e.g. `chromedriver.exe` if you're running Windows) in the PrediChord folder as well. 

PrediChord's dependencies are specified in the `requirements.txt` file included in the folder. You can install all required dependences using the following `pip` command. 

`pip install -r requirements.txt`

## Features

* Transpose a note or chord using any (positive or negative) interval.
* Find the notes belonging to many commonly used chords. 
* Write a midi file playing any given sequence of (commonly used) chords back to you.
* Scrape chords from an ultimate-guitar.com webpage. 
* Find the (likeliest) best version of the chords of a song on ultimate-guitar.com.
* Train a bi- or trigram model, and use it to generate a chord based on the input chord(s) you choose.
* Also includes: a table of the frequencies and wavelengths belonging to the pitches C0 up to and including B8. 

To-do list:
* Implement weighting mechanisms for the chords (such as TD-IDF). 
* Implement other commonly used prediction models. 
* Possibly melody and/or rhythm generation in the further future.

## Examples of use

## Project status

In development.

## Contact
Created by [Eva de Schipper](https://github.com/Evadeschipper) & [Janne Holopainen](https://github.com/Manezki).

