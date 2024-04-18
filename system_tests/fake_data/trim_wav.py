import os
from scipy.io import wavfile
from scenarios import SCENARIOS


def parse_timestamp(filename):
    """Extract and return the timestamp from the filename."""
    name_part = filename.split(
        "_")[1]  # Get the part after the first underscore
    # Convert the timestamp part to float
    timestamp = float(name_part.split(".wav")[0])
    print(f"Timestamp for {filename}: {timestamp}")
    return timestamp


def calculate_samples(duration, sample_rate):
    """
    Calculate the number of samples to trim based on the timestamps and
    sample rate.
    """
    trim_samples = int(duration * sample_rate)
    return max(trim_samples, 0)


def trim_and_save_audio(file_path,
                        trim_total,
                        trim_from_start,
                        output_folder,
                        trimmed_name):
    """
    Trim the specified number of samples from the start and save to the
    output folder.
    """
    sample_rate, data = wavfile.read(file_path)
    trim_total_samples = calculate_samples(trim_total, sample_rate)
    trim_start_samples = calculate_samples(trim_from_start, sample_rate)
    trim_end_samples = trim_total_samples - trim_start_samples
    trimmed_data = data[trim_start_samples:]
    trimmed_data = trimmed_data[:len(trimmed_data) - trim_end_samples]

    new_filename = os.path.join(output_folder, trimmed_name)
    wavfile.write(open(new_filename, 'wb'), sample_rate, trimmed_data)
    print(f"Saved trimmed audio to: {new_filename}")


if __name__ == "__main__":

    # Paths
    test_audio = "test_audio.wav"
    output_folder = "trimmed_audio/"
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each file
    for i, scenario in enumerate(SCENARIOS):
        relative_time_arrivals = scenario.relative_time_arrivals()
        trim_total_seconds = max(relative_time_arrivals)
        for j, trim_seconds in enumerate(relative_time_arrivals):
            folder = f"{output_folder}scenario_{i + 1}/"
            file_name = f"microphone_{j + 1}.wav"
            os.makedirs(folder, exist_ok=True)
            trim_and_save_audio(test_audio,
                                trim_total_seconds,
                                trim_seconds,
                                folder,
                                file_name)
