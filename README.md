# cliTube

A simple CLI Interface to play Youtube-Videos from Windows-Powershell with `tube <Video-Title>`

## Installation

1. Your file-extensions `.py` have to be associated with Python (**>= 3.6**). If you used the Windows-Installer, that should already be the case (else look that up in the [official docs](https://docs.python.org/3/faq/windows.html#how-do-i-make-python-scripts-executable)).

2. A valid installation of [VLC media player](http://www.videolan.org/vlc/) in your path-environment is required.

3. If you already have a GOOGLE-DEVELOPER-API-KEY you may skip this step. Otherwise you need to [register your own API-KEY](https://developers.google.com/youtube/android/player/register) to gain Access to the required YouTube Data API.

4. Have the google-api-client for Python installed.

    ```shell
    pip install google-api-python-client
    ```

5. Place [cliTube.py](https://raw.githubusercontent.com/oryon-dominik/cliTube/master/cliTube.py) in a directory of your choice.
6. Create a file named `secret.py` in the same directory and enter the API-Key generated above.

    ```secret.py
    DEVELOPER_KEY = '<your secret GOOGLE-API key>'
    ```

7. Add the directory of your choice to the PATH environment variable.
    Click [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) for a tutorial on how-to modify your windows-10 PATH accordingly or modify and execute the powershell-commands below for your needs.

    ```powershell
    $user_env = [Environment]::GetEnvironmentVariable("PATH", "User")
    $cliTube_path = "C:\Users\<username>\Documents\Scripts\cliTube"
    [Environment]::SetEnvironmentVariable("PATH", "$user_env;$cliTube_path", "User")
    ```

    Alternatively you could just set an Alias.

    ```powershell
    Set-Alias -Name tube -Value <your_path>/cliTube.py -Description "Plays Youtube Search-Results"
    ```

## Usage

Type `cliTube.py <The Video-Title you want to play>`

If there are several matches, cliTube will randomly select which video to play. If you don't like this "feature" modify the code for your needs accordingly. (You could set the probabilities in the function `choose` to `probabilities = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]` to always play the first match)

Have fun tubing!
