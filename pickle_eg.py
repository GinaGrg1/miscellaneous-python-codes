import pickle

imelda = ('More Mayhem',
          'Imelda May',
          '2011',
          ((1, 'Pulling the rug'),
           (2, 'Psycho'),
           (3, 'Mayhem'),
           (4, 'Kentish Town Waltz')))

# create a binary file first.
with open("Imelda.pickle", "wb") as pickle_file:
    pickle.dump(imelda, pickle_file)


with open("Imelda.pickle", "rb") as imelda_pickle:
    imelda2 = pickle.load(imelda_pickle)


print(imelda2)
album, artist, year, track_list = imelda2

for track in track_list:
    track_number, track_title = track
    print(track_number, track_title)