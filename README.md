# cliTube

A simple CLI Interface to play Youtube-Videos from Windows-Powershell with `tube <Video-Title>`

## Installation

1. Your file-extensions `.py` have to be associated to run as scripts with python (**>= 3.6**). If you used the Windows-Installer, that should already be the case (else look that up in the [official docs](https://docs.python.org/3/faq/windows.html#how-do-i-make-python-scripts-executable)). You could also just make a binary yourself.

2. A valid installation of [VLC media player](http://www.videolan.org/vlc/) in your path-environment is required.

3. If you already have a GOOGLE-DEVELOPER-API-KEY you may skip this step. Otherwise you need to [register your own API-KEY](https://developers.google.com/youtube/android/player/register) to gain Access to the required YouTube Data API.

4. Have the google-api-client for Python installed.

    ```shell
    pip install google-api-python-client
    ```

5. Place [cliTube.py](https://raw.githubusercontent.com/oryon-dominik/cliTube/master/cliTube.py) in a directory of your choice (e.g: `"$env:home\bin"`). Ensure that directory is on `PATH`.

    ```powershell
    $path = [Environment]::GetEnvironmentVariable("PATH", "User")
    $script_binaries = "env:home\bin"
    [Environment]::SetEnvironmentVariable("PATH", "$path;$script_binaries", "User")
    ```

6. Set the `GOOGLE_DEVELOPER_KEY` environment variable

    ```powershell
    [Environment]::SetEnvironmentVariable(
        "GOOGLE_DEVELOPER_KEY",
        'your secret GOOGLE-API key',
        [System.EnvironmentVariableTarget]::User
    )
    ```

    Alternatively you could just set an alias.

    ```powershell
    Set-Alias -Name tube -Value $env:home\bin\cliTube.py -Description "Plays Youtube Search-Results"
    ```

## Usage

Type `cliTube.py <The Video-Title you want to play>` or just `tube <searchterm>` with alias set.

If there are several matches, cliTube will randomly select which video to play. If you don't like this "feature" modify the code for your needs accordingly. (You could set the probabilities in the function `choose` to `probabilities = [1, 0, 0, 0, 0, 0, 0, 0, 0, 0]` to always play the first match)

Have fun tubing!
