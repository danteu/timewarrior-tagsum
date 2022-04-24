# timewarrior-tagsum

timewarrior extension that prints the total length of time spent on each of the selected tags in the selected time frame.

## Installation

```console
curl https://raw.githubusercontent.com/danteu/timewarrior-tagsum/main/tagsum.py > ~/.timewarrior/extensions/tagsum.py && \
chmod +x ~/.timewarrior/extensions/tagsum.py
```

## Usage

```console
timew tagsum [range] [tag]
```

### Example

```console
~ timew summary :ids

Wk  Date       Day ID Tags           Start      End    Time   Total
W16 2022-04-23 Sat @3 First Task   9:00:00 11:00:00 2:00:00
                   @2 Second Task 11:00:00 12:30:00 1:30:00
                   @1 First Task  13:25:42        - 4:00:02 7:30:02

                                                            7:30:02

~ timew tagsum today
First Task  -- 6:00:11
Second Task -- 1:30:00
```
