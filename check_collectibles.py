r"""List the Silent Hill: Townfall collectibles still missing for achievements.

Reads the save folder (default: %LOCALAPPDATA%\Townfall\Saved\SaveGames):
  - ProfileData.sav   : cumulative progress across all playthroughs
                        (documents, CRTV/VHF signals, phone numbers, containers)

Usage: python townfall_missing_collectibles.py [save_folder] [--all]
       --all   also list collectibles already found
"""
import glob
import os
import struct
import sys

DOCUMENTS = [
    ('379', 'Atlas Square Apartment Note'),
    ('452', 'Auxiliary Lines'),
    ('31e', 'Boat Tour Cancelled Notice'),
    ('2f3', 'Box IDs and Names'),
    ('3d5', 'CEG Checkout Sheet'),
    ('367', 'CEG Employee Locker List'),
    ('376', 'CEG Kiosk Note'),
    ('37a', 'CEG Lockers Managers Note'),
    ('377', 'CEG Memo'),
    ('2fd', 'CEG Security: Out of Hours Access'),
    ('36c', 'CEG Tower Meeting Minutes'),
    ('397', 'CEG Tower: Engineer Public Statement'),
    ('396', 'CEG Tower: Evening News'),
    ('45e', "CEG Tower: He's Done"),
    ('45f', 'CEG Tower: What did you do?'),
    ('38a', 'Clamp Release Procedure'),
    ('308', 'Clinic Email: "Where Are You?"'),
    ('41b', 'Clinic Email: Reception Answer Phone Message'),
    ('407', 'Community Help Needed'),
    ('2ca', 'Complete Grid of Codes'),
    ('115', 'Construction Halted Notice'),
    ('1ec', 'Crew Patch'),
    ('3fd', 'Current Count'),
    ('40c', 'Dailies - Infusion Status'),
    ('2c0', 'Employee File Cover Note'),
    ('d5', 'Equipment Cleanup Notice'),
    ('408', 'Exhausted Supplies'),
    ('234', 'Facilities: "DONTREAD.DOC"'),
    ('2ed', 'Facilities: Works Halted'),
    ('375', 'Feeling Sick Note'),
    ('3cc', 'Gaming Magazine'),
    ('2c9', 'Grid of Codes (large)'),
    ('2c8', 'Grid of Codes (small)'),
    ('186', 'Hand Delivered Letter'),
    ('d1', 'Handwritten Note'),
    ('31f', 'Harbour Notice'),
    ('26c', 'Hotel Reception Notice'),
    ('353', 'Hotel Room Note'),
    ('2cd', 'Inquiry Preparation Notice'),
    ('152', 'Jane Chalmers Obituary'),
    ('18c', 'Jess Legal Advice'),
    ('41a', "Jess's Door Note"),
    ('41c', 'Lamenting Poem'),
    ('317', 'Lost and Found'),
    ('190', 'Medical Security Note'),
    ('37c', 'Newsagents Note'),
    ('335', 'Note on Patient Records'),
    ('88', "Nurse's Rounds Form"),
    ('459', 'Ordell File'),
    ('279', 'Organ Transplant Card'),
    ('434', 'Photo of Joe McKenzie'),
    ('e1', 'Photo1.jpg'),
    ('1f6', 'Photo2.jpg'),
    ('3dd', 'Power Card Credit Guide'),
    ('36d', 'PR Meeting Note'),
    ('23c', 'Press Photos "Note.txt"'),
    ('436', 'RCU Refit Note'),
    ('40a', 'RE: Supply Situation Update'),
    ('3cd', 'Reciprocating Compressor'),
    ('40f', 'Records Room Code'),
    ('3c7', 'Reference Sheet'),
    ('439', 'Remote Systems Control'),
    ('27d', 'Resignation Letter'),
    ('281', 'Restock Issues'),
    ('348', "Richard's Note"),
    ('3f9', 'Room Service Card'),
    ('395', 'Scaffold Notice'),
    ('71', 'Shorefront Family Clinic Notice'),
    ('181', 'St. Amelia Standard'),
    ('b', 'Store Staff Notice'),
    ('409', 'Supply Situation Update'),
    ('460', 'SWDP: Ordell Site Visit'),
    ('292', 'Task Assignment'),
    ('3f7', 'The Code After'),
    ('3f6', 'The Code Before'),
    ('400', 'The Code Today'),
    ('40b', 'Unrealistic Expectations (number 1098512....)'),
    ('2fe', 'Urgent Message'),
    ('6f', 'Vigil & Protest Flyer'),
    ('2df', 'Water Warning'),
    ('299', 'Zoe\'s Email: "Coming Back"'),
    ('228', 'Zoe\'s Email: "For Attending..."'),
    ('27b', 'Zoe\'s Email: "Please Report In"'),
    ('226', 'Zoe\'s Email: "Your Letter"'),
    ('3de', "Zoe's Patient List"),
]

CRTV_SIGNALS = [
    ('288', 'Come Back To Me Simon'),
    ('287', 'Hotel Room'),
    ('3fb', 'Hotel Room 2'),
    ('28b', 'Medical Centre'),
    ('450', 'Missing Parts: 10th Floor'),
    ('44f', 'Missing Parts: Help'),
    ('44e', 'Missing Parts: Lockers'),
    ('456', 'Missing Parts: Together'),
    ('457', 'Missing Parts: Where'),
    ('284', 'Return To Clinic'),
]

VHF_SIGNALS = [
    ('25c', 'Apartment'),
    ('3f1', 'CEG Atrium'),
    ('435', 'I know what you saw'),
    ('455', 'Many Into One'),
    ('296', 'Pharmacy'),
    ('378', 'Richard and the Board'),
    ('2d1', 'South Brae Paperwork'),
    ('437', 'Supermarket Handouts'),
    ('3e0', 'Vent Safe House'),
]

POSTCARDS = [
    ('43a', 'Strange Postcard - 1'),
    ('43b', 'Strange Postcard - 2'),
    ('453', 'Strange Postcard - 3'),
    ('43c', 'Strange Postcard - 4'),
    ('43d', 'Strange Postcard - 5'),
    ('43e', 'Strange Postcard - 6'),
    ('43f', 'Strange Postcard - 7'),
    ('445', 'Strange Postcard - 8'),
    ('446', 'Strange Postcard - 9'),
    ('440', 'Strange Postcard - 10'),
    ('441', 'Strange Postcard - 11'),
    ('442', 'Strange Postcard - 12'),
    ('443', 'Strange Postcard - 13'),
    ('444', 'Strange Postcard - 14'),
    ('447', 'Strange Postcard - 15'),
]

PHONE_NUMBERS = [
    (1, '010', 'Operator'),
    (2, '900', 'Emergency'),
    (3, '4960496', 'Tourist Centre'),
    (4, '01632960595', 'St. Amelia District Council'),
    (5, '4960244', 'The Haldane Hotel'),
    (6, '946', 'W H O Dial Back Service'),
    (7, '100', '"Save Yourself"'),
    (8, '5353', 'Hospital Storage'),
    (9, '4960556', 'Dr. Glenn'),
    (10, '4960112', 'Unknown'),
    (11, '4960103', 'Zoe Ellis'),
    (12, '4960842', 'Unknown'),
    (13, '4960993', 'CEG Lockers'),
]

KNOWN_CONTAINERS = ["LockBoxA", "LockBoxB", "LockBoxC", "LockBoxD", "LockBoxE", "LockBoxF", "LockBoxG"]

class Reader:
    def __init__(self, data, pos=0):
        self.data, self.pos = data, pos

    def i32(self):
        v = struct.unpack_from("<i", self.data, self.pos)[0]
        self.pos += 4
        return v

    def u8(self):
        v = self.data[self.pos]
        self.pos += 1
        return v

    def fstring(self):
        n = self.i32()
        if n == 0:
            return ""
        if n < 0:
            raw = self.data[self.pos:self.pos - 2 * n]
            self.pos -= 2 * n
            return raw.decode("utf-16-le").rstrip("\0")
        raw = self.data[self.pos:self.pos + n]
        self.pos += n
        return raw[:-1].decode("utf-8", "replace")

    def type_name(self):
        name = self.fstring()
        params = [self.type_name() for _ in range(self.i32())]
        return name, params


VALUE_READERS = {
    "BoolProperty": lambda r: r.u8() != 0,
    "IntProperty": lambda r: r.i32(),
    "StrProperty": lambda r: r.fstring(),
    "NameProperty": lambda r: r.fstring(),
}


def read_map(data, map_name):
    """Return the named top-level map as a dict (empty if absent)."""
    encoded = map_name.encode() + b"\0"
    needle = struct.pack("<i", len(encoded)) + encoded
    start = data.find(needle)
    if start < 0:
        return {}
    r = Reader(data, start)
    r.fstring()
    type_name, params = r.type_name()
    if type_name != "MapProperty" or len(params) != 2:
        return {}
    read_key = VALUE_READERS.get(params[0][0])
    read_value = VALUE_READERS.get(params[1][0])
    if not read_key or not read_value:
        return {}
    r.i32()
    r.u8()
    r.i32()
    result = {}
    for _ in range(r.i32()):
        key = read_key(r)
        result[key] = read_value(r)
    return result


def read_save(path):
    with open(path, "rb") as f:
        data = f.read()
    if not data.startswith(b"GVAS"):
        raise ValueError("not a GVAS save file")
    return {name: read_map(data, name) for name in ("SavedBoolMap", "SavedIntMap", "SavedStringMap")}


def values_with_prefix(string_map, prefix):
    return {v for k, v in string_map.items() if k.startswith(prefix)}


def print_section(title, achievement, entries, show_all, note=None):
    found = sum(1 for _, ok in entries if ok)
    print(f"\n== {title}: {found}/{len(entries)}   [{achievement}]")
    if note:
        print(f"   ({note})")
    if found == len(entries):
        print("   All found!")
    for label, ok in entries:
        if show_all or not ok:
            print(f"   {'[x]' if ok else '[ ]'} {label}")


def report_profile(folder, show_all):
    path = os.path.join(folder, "ProfileData.sav")
    if not os.path.isfile(path):
        print(f"ProfileData.sav not found in {folder}")
        return
    save = read_save(path)
    strings, ints = save["SavedStringMap"], save["SavedIntMap"]

    print("#" * 70)
    print("# PROFILE (cumulative across all playthroughs)")
    print("#" * 70)

    docs = values_with_prefix(strings, "Total_DiscoveriesFound_")
    print_section("Documents", "Observation 50% / Thorough Inspection",
                  [(name, i in docs) for i, name in DOCUMENTS], show_all)

    crtv = values_with_prefix(strings, "Total_WaypointSignalsTuned_")
    print_section("CRTV signals", "Sweeping Signals",
                  [(name, i in crtv) for i, name in CRTV_SIGNALS], show_all)

    vhf = values_with_prefix(strings, "Total_TransceiversTuned_")
    print_section("VHF transmissions", "Sweeping Signals?",
                  [(name, i in vhf) for i, name in VHF_SIGNALS], show_all)

    mask = ints.get("Total_PhoneNumbersCalledBitmask", 0)
    print_section("Phone numbers", "Cold Calling",
                  [(f"{name} ({number})", (mask >> bit) & 1 == 1) for bit, number, name in PHONE_NUMBERS],
                  show_all)

    opened = values_with_prefix(strings, "Total_ResourceContainersUnlocked_")
    containers = KNOWN_CONTAINERS + sorted(opened - set(KNOWN_CONTAINERS))
    print_section("Resource containers", "Resourceful",
                  [(c.replace("LockBox", "Lock box "), c in opened) for c in containers], show_all,
                  note="game doesn't name them, but they should be in order of appearance A-G")


def postcards_in_save(save):
    bools, strings = save["SavedBoolMap"], save["SavedStringMap"]
    ids = set()
    for key, value in bools.items():
        if value and key.startswith("TFIC_DiscoveredByPlayer_"):
            ids.add(key.rsplit("_", 1)[1])
    for key, value in strings.items():
        if key.startswith("TFPC_TFIC_") and key.endswith("_ID"):
            ids.add(value)
    return ids


def report_playthroughs(folder, show_all):
    paths = sorted(glob.glob(os.path.join(folder, "SaveGame*.sav")))
    if not paths:
        print("No SaveGame*.sav found.")
        return
    known = {i for i, _ in POSTCARDS}
    best_path, best_ids = None, set()
    for path in paths:
        try:
            ids = postcards_in_save(read_save(path)) & known
        except (ValueError, struct.error) as e:
            print(f"\n{os.path.basename(path)}: unreadable ({e})")
            continue
        # Ties go to the most recently modified save.
        if best_path is None or len(ids) > len(best_ids) or (
                len(ids) == len(best_ids) and os.path.getmtime(path) > os.path.getmtime(best_path)):
            best_path, best_ids = path, ids
    if best_path is None:
        print("No readable SaveGame*.sav found.")
        return
    print_section("Strange postcards", "Blur Your Eyes",
                  [(name, i in best_ids) for i, name in POSTCARDS], show_all)


def main():
    args = [a for a in sys.argv[1:] if a != "--all"]
    show_all = "--all" in sys.argv[1:]
    default = os.path.join(os.environ.get("LOCALAPPDATA", ""), "Townfall", "Saved", "SaveGames")
    folder = os.path.expandvars(args[0]) if args else default
    if not os.path.isdir(folder):
        print(f"Save folder not found: {folder}", file=sys.stderr)
        return 1
    print(f"Save folder: {folder}")
    report_profile(folder, show_all)
    report_playthroughs(folder, show_all)
    return 0


if __name__ == "__main__":
    try:
        status = main()
    except Exception:
        import traceback
        traceback.print_exc()
        status = 1
    # Keep the console open when the .exe is launched by double-click.
    if getattr(sys, "frozen", False):
        input("\nPress Enter to close...")
    sys.exit(status)