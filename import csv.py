import csv

# Input and output files
amc_file = "AMC File #15.txt"
csv_file = "joint_angles.csv"

# Joints to extract
joints = ["lradius","rradius","rhumerus", "lhumerus", "rwrist", "lwrist","lfemur","rfemur","rtibia","ltibia","rfoot","lfoot","root","rclavicle","lclavicle","lhand","rhand"]

with open(amc_file, "r") as f:
    lines = f.readlines()

data = []
frame = None
frame_data = {}

for line in lines:
    line = line.strip()
    if line.isdigit():  # New frame
        if frame_data:
            data.append(frame_data)
        frame = int(line)
        frame_data = {"frame": frame}
    else:
        parts = line.split()
        if parts[0] in joints:
            # Convert the rest of the values to float
            values = list(map(float, parts[1:]))
            frame_data[parts[0]] = values

# Append the last frame
if frame_data:
    data.append(frame_data)

# Write to CSV
with open(csv_file, "w", newline="") as f:
    writer = csv.writer(f)
    # Header
    header = ["frame"]
    for joint in joints:
        # Assume up to 3 values per joint
        for i in range(3):
            header.append(f"{joint}_{i+1}")
    writer.writerow(header)

    # Rows
    for frame_data in data:
        row = [frame_data["frame"]]
        for joint in joints:
            vals = frame_data.get(joint, [None]*3)
            # Pad to 3 values
            vals += [None]*(3-len(vals))
            row.extend(vals)
        writer.writerow(row)

print(f"Data exported to {csv_file}")


