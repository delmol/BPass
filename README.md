# BPass

## Introduction

BPass is a very basic demo of a deterministic password generator/manager using cryptography.

As it stands this program is very simple and very insecure (it only uses 28 bits of entropy) and shouldn't be used for anything other than demostration purpose only. It was made simply as a proof of concept to show how a deterministic password generator could work.

BPass will generate you a master password in the form of a 7 word mnemonic phrase

> jungle banana nature dentist february endless abstract

Using this master password, you can generate any number of 32 character passwords deterministically. 

Meaning that given the same master password (mnemonic), it is possible to regenerate the same password every time without the need for storing any external data.

## Usage

To use the program simply run through your terminal

> python bpass.py

This will generate you a new mnemonic master password

To generate passwords using your mnemonic, run the program again supplying your mnemonic

> python bpass.py "jungle banana nature dentist february endless abstract"

Note: Currently there are no checks on data input. Make sure your mnemonic is in lower case, has a space between each word and contains no extra spaces at the beginning or end.

## How it works

### Generating a master seed

First, a master seed is generated which will be used to generate the mnemonic.

24 bits (3 bytes) of entropy are generated by the OS as our main source of entropy. In a production setting this would be much higher (256 bits+), but for the sake of simplicity and keeping the word list relatively short, we will use only 24 bits.

In all, two sources of 24 bit entropy are generated and converted to hexidecimal string. One will be used as our main source of entropy, the second for our salt used later.

The entropy is converted to a hexidecimal string and hashed with [PBKDF2](https://en.wikipedia.org/wiki/Pbkdf2). SHA512 is used as the pseudo-random function, the hex entropy is used as the password, the salt entropy hashed with SHA256 is used as the salt, and we will iterate 2048 times.

It's not a good idea to hold onto the initial entropy, and I didn't want it to be possible to derive the initial entropy from the mnemonic. So a one way function is used to prevent that. Although ultimately it doesn't make much difference either way.

Once this is complete we will have a master seed:

> 9041c28570fa504f20d5d41d342a49c46289976f8b0904b68ca25494af982ee14a31921027e0eb86822998399aec3df4331e378218732c0b293ffdb980ad515b

For the sake of this demo we're going to chop this down to simply 6 characters, or 24 bits. In production you'd probably want to use the entire seed.

So we're left with:

> 9041c2

The next step is to create a checksum and append it to the end of the seed. This is simply so that later on when a mnemonic seed is entered, we can verify the legitimacy of the mnemonic.

The seed is hashed using SHA256 to create a checksum of the seed:

> EBD1E0E4D7C145287C65AB7311AD6BDD9F2C5325F23F13EA3396F645A416E1C1

We will then take the first character (4 bits) and append it to our seed. So our seed should now look like this:

> 9041c2e

There we have it, we now have our master seed from which we'll dervive our mnemonic phrase. The user doesn't ever need to know their master seed, but importantly the seed can always be dervived from the mnemonic phrase.

### Generating a mnemonic phrase

Now we have our seed, the mnemonic phrase can be generated from the seed.

This process is relatively simple. We can treat each hexidecimal character of the seed as a number that corresponds to our word list.

For this demo I'm only using one character, or 4 bytes. Simply because each character represents a number between 0 and 15, we can keep our wordlist short. In practice you'd want to use many more bytes of data to have thousands or tens of thousands of possible words.

So we take our master seed, split it up into individual characters (or 4 bit chunks) and convert each hexidecimal character to a decimal integer.

> 9, 0, 4, 1, 12, 2, 14

And then assign those numbers to a word in the word list (see wordlist.py)

> industry rhythm dentist abstract lecture banana nature

And there we have it, our master password or mnemonic phrase.

### Decrypting the mnemonic

Once the user has a mnemonic master password, we need to be able to decrypt the password back into it's original seed so we can generate passwords from it.

So we just do the same thing in reverse.

Convert the words back into numbers, and then from numbers to hexidecimal characters, which gives the master seed.

The beauty of this is it requires no data to be saved whatsoever. So this can be performed anywhere, indepedent of the device. We can generate a mnemonic on one device, and generate passwords on another.

### Generating passwords

Now that we have a master password, we can now use that password to generate password from it deterministically. So that given the same password and salt we will always generate the same password.

We will generate a new seed from our master seed to create passwords with.

We throw our seed back into our PBKDF2 function toget a new password seed. This time using our mnemonic as the password and salt.

> Master seed: 9041c2e
> 
> Password seed: d634aff2d54ad209f3a6990be9022b6b8140d00cdf027fecc36a3691dfa25c2a6925b0c258100cf420e7f9d40544e203cb888a5c3d1b38a37de0d9c735c21be4

Now, you might quite rightly ask what is the need for hashing yet another seed to generate passwords from? Honestly, I don't know. It was late at night when I was writing this program and I have no idea why I did it that way.

Now we've got the new seed, we can generate password from it.

For simplicity I just went with throwing the trusty seed + salt format through SHA256. Where the name of the website/service is the salt.

I thought this was quite an ingenious solution. The problem I came across was that if you used some sort of deterministic sequence (e.g. numbers - 1, 2, 3, 4) you'd need to store the name of whatever password you were using as a separate file which wouldn't work across multiple devices.

You'd just end up with a list of passwords, and no idea which password was used for what.

But, if you used the site name, or something similar, it would be very easy to remember. It's much easier to type "github" and get your github password. And you can store multiple - github1, github2.

Obviously this is just a demo, but in a fully fledged GUI implementation that could quite easily be worked out.

> SHA256( [Password Seed] + [Salt] ) = password
> 
> d634aff2d54ad209f... + "github"
> 
> Password: 5A4CD9ACE8435CCED64F3D85D9ED329D5EB4460A296A82095C328DC4E8442A80

Not many service will accept a 64 character password, so BPass will cut down the password to 32 character

> Password: 5a4cd9ace8435cced64f3d85d9ed329d

Now we have our deterministic password generated from a mnemonic phrase.

The user can now go onto another computer, enter that same mnemonic, the same salt (github) and get the same password.
