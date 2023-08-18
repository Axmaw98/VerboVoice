# VerboVoice
VerboVoice allows seamless entry of prompts, generating corresponding speech, and easy playback control. It supports various features like audio generation, playback, and deletion, while offering a sleek design and simple user experience.

This is a PyQt5-based graphical user interface (GUI) application that allows users to generate answers based on the entered prompt and then convert the answer from You.com's API into speech using the Edge TTS API. The application provides a user-friendly interface for entering text prompts, generating corresponding speech, and controlling playback. It utilizes the Edge TTS API for text-to-speech conversion and incorporates various GUI elements for interaction.

![Screenshot](https://github.com/Axmaw98/VerboVoice/assets/90964275/38addc2f-e922-4826-9a3b-dda91668c754)

## Table of Contents

- [Features](#features)
- [Usage](#usage)
- [How It Works](#how-it-works)
- [Dependencies](#dependencies)
- [Contributing](#contributing)
- [License](#license)

## Features

1. Input Field: Enter the desired text prompt for speech generation.
2. Title Field: Provide a title for the generated audio file.
3. Output Field: Displays the status of the audio generation process and playback controls.
4. Playback Controls:
   - Play: Start playback of the generated audio.
   - Pause: Pause the audio playback.
   - Stop: Stop the audio playback.
   - Delete: Delete the generated audio file.
5. Generate MP3 Button: Initiate the process of generating the speech audio from the entered text prompt.
6. Minimize/Close Buttons: Minimize or close the application window.

## Usage

1. Run the application.
2. The application window will appear, providing an interface to interact with the text-to-speech functionality.
3. Enter your desired text prompt in the input field and provide a title for the generated audio file.
4. Click the "Generate MP3" button to initiate the speech generation process.
5. Once the generation is complete, the application will display the status and enable playback controls.
6. Once the generation is complete, the application will display the status and enable playback controls.
7. Use the playback controls (Play, Pause, Stop) to interact with the generated audio.
8. Click the "Delete" button to remove the generated audio file.
9. To close the application, click the close button or use the system window controls.

## How It Works

The application utilizes PyQt5 for creating the graphical user interface and incorporating various GUI elements such as text input fields, buttons, and labels. It communicates with the Edge TTS API to convert the answer from You.com's API into speech audio files.

When the "Generate MP3" button is clicked, the application sends the entered text prompt to You.com's API and then the retrieved answer will be sent to the Edge TTS API in order to generate audio. It then saves the audio as an MP3 file with the specified title and sets up a media player for playback. Users can control playback using the provided playback controls.

The application features drag-and-drop functionality to move the window and a customized window design using CSS styling.


## Dependencies

- PyQt5: GUI framework for creating the application interface.
- you: Python library for interacting with the "You.com" API.
- Edge TTS: API for text-to-speech conversion.
- asyncio: Asynchronous programming library for handling concurrent tasks.

## Contributing

Contributions are welcome! If you find a bug or have suggestions for improvements, feel free to open an issue or submit a pull request. Please make sure to adhere to the existing code style and guidelines.

## Credit

The "you" library used in this project is authored by [An Author](link-to-author-profile). Full credits and acknowledgments for the "you" library will be added to this section very soon.


## License

This project is licensed under the [GNU General Public License version 3.0 (GPL-3.0)](https://github.com/Axmaw98/VerboVoice/blob/main/LICENSE). You are free to use, modify, and distribute the code as long as you adhere to the terms and conditions of the GPL-3.0 license. This license ensures that derivative works are also open source and under the same terms, promoting the free distribution and modification of software.


