# ClubLogLeague

Python script to download the latest DXCC league table from [ClubLog.org](https://clublog.org).

The script makes use of the ClubLog API to download the latest DXCC league table from all collected data. 
No authentication is required to use this portion of the API so you will not need an account or API key.

Details of the API used can be found at [APIs and Integration Notes - Downloading DXCC leagues as JSON](https://clublog.freshdesk.com/support/solutions/articles/3000054404-downloading-dxcc-leagues-as-json).

## Usage

Simply run the script or one of the executables from a command prompt/terminal. With no option specified the global league will be downloaded and saved as `league.csv`.  

The following arguments can be used to further refine the data set to your liking:

  | Option             | Values                                     | Default        | Description                                                                                                                                              |
  | ------------------ | ------------------------------------------ | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
  | `-h`, `--help`     |                                            |                | Show the help message and exit.                                                                                                                          |
  | `-o`, `--csv_file` | `PATH`                                     | `./league.csv` | The path to write the CSV file to.                                                                                                                       |
  | `-m`, `--mode`     | `All`, `CW`, `Phone`, `Data`               | `All`          | Filter by mode.                                                                                                                                          |
  | `-q`, `--qsl`      | `Worked`, `Confirmed`                      | `Worked`       | Filter by worked or confirmed status.                                                                                                                    |
  | `-d`, `--date`     | `All`, `Past12`, `CurrentYear`, `LastYear` | `All`          | Filter by date.                                                                                                                                          |
  | `-c`, `--club`     | `ID`                                       | `0`            | Filter by club, defaults to global list.Must be the ID number for the desired club.See https://tinyurl.com/ybs9zx7n for details of how to obtain the ID. | 
  | `-D`, `--deleted`  | `Current`, `All`                           | `Current`      | Filter by inclusion of deleted entries.                                                                                                                  |
  | `-e`, `--exclude`  | `CALL ...`                                 |                | Removes the specified calls from the results.                                                                                                            |

## Generating Executables

For ease of use the script in this repo can be compiled to an executable for both Linux and Windows through the 
use of [PyInstaller](https://www.pyinstaller.org).

### Required Software

To build packages for Linux from a Linux environment you will need:

  - [Python](https://python.org)

To build executable files for Windows from a Linux environment you will need:

  - [Oracle VirtualBox](https://www.virtualbox.org)
  - [HashiCorp Vagrant](https://www.vagrantup.com)

### Running the Build Scripts
The `build-scripts` directory contains a set of files for building executables for Windows and Linux.

  | Name                           | Target  | Dev Environment | Vagrant |
  | ------------------------------ | ------- | --------------- | :-----: |
  | `build-executable-linux.sh`    | Linux   | Linux           | N       |
  | `build-executable-window.sh`   | Windows | Linux           | Y       |
  | `build-executable-windows.bat` | Windows | Windows         | N       |

These scripts make use of a Python Virtual Environment and PyInstaller to generate executables for their target environment.

When the *Target* and *Dev Environment* do not match for a script a Vagrant box is used to spin up the relevant 
*Dev Environment* inside of a Virtual Machine. This allows for executables to be built for both environments from 
both environment. 

To build an executable just run the relevant script for the target and development environment, no parameters are required.
The scripts will place the executables into the `./executables` directory after building.

## Authors

* **Antony Jordan [2E0KXV]** - *Initial work*

See also the list of [contributors](https://github.com/wiccan2/ClubLogLeague/contributors) who participated in this project.

## License

[![WTFPL](http://www.wtfpl.net/wp-content/uploads/2012/12/wtfpl-badge-4.png)](http://www.wtfpl.net/)

This project is licensed under the WTFPL License - see the [COPYING](COPYING) file for details
