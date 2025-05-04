<br>
<div align="center">
    <img src="icon.svg" width="80" height="80">
    <h3>Anki Spell Checker</h3>
    <p>A simple add-on to check for spelling mistakes when you are editing your cards.</p>
    <a href="https://github.com/EKHH/anki-spell-checker/releases/download/v1.0.0/anki-spell-check.ankiaddon">
    <strong>Download »</strong>
    </a>
    <br>
</div>

### Features

> [!IMPORTANT]
> This add-on only works on Windows and Linux; macOS is not yet supported.

- Supports multiple languages.
- Supports customized dictionaries.
- Minimalistic design; no flashy things.

### Installation

1. Double-click the downloaded `.ankiaddon` file.
2. Follow the installation prompt; restart Anki if it asks you to.
3. Read the sections below to configure the add-on.

### Setup

#### Basic

This add-on relies on dictionary files for checking spelling mistakes. As such, it is able to download those files for some common languages.

1. Navigate to `Tools` > `Add-ons` and click the `Anki Spell Checker` entry twice.
2. Select your preferred language(s) from the list and click the `Enable` button.
3. If the selected item turns green, the dictionary has been downloaded.

You may disable the spell checker for certain dictionaries by clicking the `Disable` button after you have selected them.

> [!TIP]
> To exclude a word from the spell checker permanently, select the *Add to dictionary* option in the context menu.

#### Advanced

You may incorporate your own dictionary in the following ways:

**`.txt` or `.dic` file**

> [!NOTE]
> `.txt` files must consist of one word per line. A `.aff` file is optional; if you do not supply one, no additional rules will be used.

1. Navigate to `Tools` > `Add-ons` and double-click the `Spell Checker` entry.
2. Click on the `Excluded Words` button; a folder should open.
3. Place your file in the said folder and return to the configuration window.
4. Click on the `Compile` button and reopen the configuration window.

Your dictionary should now be listed.

**`.bdic` files**

If you have a precompiled `.bdic` file, proceed as follows:

1. Navigate to `Tools` > `Add-ons` and click the `Spell Checker` entry twice.
2. Click on the `All Dictionaries` button; a folder should open.
3. Place your `.bdic` file in the folder and reopen the configuration window.

Your dictionary should now be listed.

### Acknowledgement

I do not take any credit for anything in this repository; most of it is not my work.

- This project is a derivative of [Valentin](https://github.com/ValentinSchmitz)'s [Spell Checker](https://github.com/ValentinSchmitz/spell-checker), which was based on the [Spelling Police](https://github.com/lovac42/SpellingPolice) add-on by [lovac42](https://github.com/lovac42).
- Internally, the `convert_dict` tool converts all dictionaries used for checking spelling mistakes.
  - On Linux distributions, the [binaries](https://github.com/jankelemen/convert-dict-tool-from-chromium) for this tool are provided by [Jan Kelemen](https://github.com/jankelemen).
  - On Windows, the [binaries](https://github.com/jmbeach/convert_dict_windows) for this tool are provided by [Jared Beach](https://github.com/jmbeach).
- The actual dictionaries are downloaded from [Titus Wormer](https://github.com/wooorm)'s [repository](https://github.com/wooorm/dictionaries) under [various licenses](https://github.com/wooorm/dictionaries#list-of-dictionaries).
- The `addToDictionary`, `compileBDIC`, and `needCompileAnkiStartUp` functions were created by [Shigeyuki](https://github.com/shigeyukey) as part of the [Anki Spell Checker](https://ankiweb.net/shared/info/143753963) add-on.
- All of the aforementioned projects are made available under the [GNU General Public License, Version 3](https://opensource.org/license/gpl-3-0).
- The icon for the add-on was created as a part of the [Carbon Design System](https://github.com/carbon-design-system/carbon), which is made available under the [Apache License, Version 2.0](https://opensource.org/license/apache-2-0).
