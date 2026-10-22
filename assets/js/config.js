/* Everything you might want to change lives here: dates, rates, bookings, contact, photos, places.
   Dates are YYYY-MM-DD. After editing, commit and push; the page and the card update themselves. */
window.SITE = {
  // Shown on the postmark and in every enquiry ("<town> holiday home, <occasion> 2026").
  // Keep town to about 16 characters so it fits around the postmark ring.
  town: 'Diaz Beach',
  occasion: 'Summer',

  // Guests can arrive from firstNight and must leave by lastCheckOut. No stay is longer than maxNights.
  season: { firstNight: '2026-11-25', lastCheckOut: '2026-12-12', maxNights: 17 },

  // Each rate runs from its minNights up to the next rate; the last one up to maxNights.
  // The shortest stay is the smallest minNights.
  rates: [
    { minNights: 7, perNight: 3000 },
  ],

  // Confirmed bookings: guests arrive on "from" and leave on "to", e.g. { from: '2026-12-19', to: '2027-01-02' }.
  booked: [],

  // ref is added as the last line of every WhatsApp and email enquiry. Leave it empty ('') to drop it.
  contact: { phone: '084 868 2186', email: 'marisajansevanvuuren3@gmail.com', ref: 'DIAZ-CARD' },

  // Gallery order, as a walk through the house. "wide" photos take a full row on phones and a 2x2 block on
  // computers; keep the plain photos between wide ones in multiples of 4 so the grid has no gaps. A wide photo placed last becomes a full-width banner.
  photos: [
    { src: 'sea-view', caption: 'Looking over the rooftops to the sea', wide: true },
    { src: 'lounge', caption: 'Lounge, through to the kitchen' },
    { src: 'lounge-balcony', caption: 'Lounge, with doors onto the balcony' },
    { src: 'lounge-tv', caption: 'Smart TV in the lounge' },
    { src: 'sleeper-couch', caption: 'Sleeper couch, with the air-conditioner above the balcony door' },
    { src: 'desk', caption: 'A desk in the corner of the lounge' },
    { src: 'kitchen', caption: 'Kitchen with a breakfast counter' },
    { src: 'kitchen-fridge', caption: 'Fridge, microwave, dishwasher and washing machine' },
    { src: 'kitchen-hob', caption: 'Four-plate hob and oven' },
    { src: 'balcony-braai', caption: 'Built-in braai on the balcony, with the sea at the end of the road', wide: true },
    { src: 'moonrise', caption: 'Full moon rising over the bay', wide: true },
    { src: 'main-bedroom', caption: 'Main bedroom, double bed' },
    { src: 'main-bedroom-2', caption: 'Main bedroom, built-in cupboards and a TV' },
    { src: 'bedroom-2', caption: 'Second bedroom, two single beds' },
    { src: 'bathroom', caption: 'Bathroom with a bath and a separate shower' },
  ],

  // The pin sits on Beach Boulevard West, not on the flat; the exact address is shared once guests book.
  home: { name: 'The flat', lat: -34.16110, lng: 22.10805, label: 'w' },

  // Map pins and the list under the map, nearest first. kind: beach | food | see.
  // label = which side of the pin the name sits on (n, s, e, w). Drive times are from the house.
  places: [
    // {
    //   id: 'museum', name: 'Town Museum', kind: 'see', lat: -34.18, lng: 22.14, label: 'w',
    //   km: 0.8, drive: 2,
    //   about: 'One or two sentences a guest would care about.',
    //   picks: [{ name: 'Museum Cafe', note: 'coffee in the garden' }],
    //   query: 'Town Museum <town>',
    // },
    {
      id: 'diaz-beach', name: 'Diaz Beach', kind: 'beach', lat: -34.16110, lng: 22.11060, label: 'e',
      km: 0.4, drive: 2,
      about: 'The beach closest to the flat, about a 6-minute walk away, and a favourite with surfers.',
      query: 'Diaz Beach Mossel Bay',
    },
    {
      id: 'water-park', name: 'Diaz Water Park', kind: 'see', lat: -34.15937, lng: 22.10923, label: 'n',
      km: 0.4, drive: 1,
      about: 'Slides, super tubes, a lazy river and a kiddies’ pool next to the Diaz Hotel, about a 6-minute walk away. It is seasonal and closes in bad weather, so phone 044 692 8400 before you go.',
      picks: [{ name: 'Bahia Bleu', note: 'restaurant in the Diaz Hotel, with a veranda looking out to sea' }],
      query: 'Diaz Water Park Mossel Bay',
    },
    {
      id: 'mall', name: 'Langeberg Mall', kind: 'see', lat: -34.14823, lng: 22.10403, label: 'e',
      km: 2.8, drive: 5,
      about: 'The nearest shopping centre, with over 100 shops and free covered parking.',
      picks: [
        { name: 'Pick n Pay', note: 'groceries' },
        { name: 'Pick n Pay Liquors', note: 'drinks for the braai' },
        { name: 'Mugg & Bean', note: 'sit-down café' },
      ],
      query: 'Langeberg Mall Mossel Bay',
    },
    {
      id: 'santos', name: 'Santos Beach', kind: 'beach', lat: -34.17706, lng: 22.13806, label: 'w',
      km: 3.6, drive: 6,
      about: 'Mossel Bay’s town beach faces north into the bay, so the water is usually calmer than at Diaz. Last season lifeguards were on duty daily from 1 December.',
      query: 'Santos Beach Mossel Bay',
    },
    {
      id: 'dias', name: 'Dias Museum', kind: 'see', lat: -34.18040, lng: 22.14210, label: 'w',
      km: 4.4, drive: 6,
      about: 'A life-size replica of Bartolomeu Dias’s caravel, plus a shell museum and an aquarium. The caravel is closed for boarding for now, but you can still see it.',
      picks: [{ name: 'Post Office Tree', note: 'the old tree where early sailors left messages' }],
      query: 'Bartolomeu Dias Museum Complex Mossel Bay',
    },
    {
      id: 'kaai-4', name: 'Kaai 4', kind: 'food', lat: -34.17862, lng: 22.14193, label: 'n',
      km: 4.8, drive: 7,
      about: 'Open-air braai restaurant by the harbour wall, built around a big fire with sand underfoot. Expect spitbraai, potjiekos, roosterkoek and fish off the grid.',
      query: 'Kaai 4 Braai Restaurant Mossel Bay',
    },
    {
      id: 'point', name: 'The Point', kind: 'see', lat: -34.18310, lng: 22.15781, label: 'w',
      km: 5.7, drive: 8,
      about: 'The tip of Cape St Blaize, with a tidal pool, the St Blaize Cave and the 1864 lighthouse. The 13.5 km St Blaize Trail starts at the cave and follows the cliffs west.',
      query: 'Point tidal pool Mossel Bay',
    },
    {
      id: 'hartenbos', name: 'Hartenbos Beach', kind: 'beach', lat: -34.12185, lng: 22.12140, label: 'e',
      km: 6.2, drive: 8,
      about: 'Swimming beach in front of the ATKV Hartenbos resort. Last season lifeguards were on duty daily from 1 December.',
      query: 'Hartenbos Beach',
    },
    {
      id: 'casino', name: 'Garden Route Casino', kind: 'see', lat: -34.19593, lng: 22.09153, label: 'e',
      km: 6.2, drive: 9,
      about: 'Casino and hotel at Pinnacle Point (18 and over to gamble), with a family buffet and live music in the lounge.',
      picks: [{ name: 'The Fun Company', note: 'mini bowling and arcade games for ages 5 and up' }],
      query: 'Garden Route Casino Mossel Bay',
    },
  ],
};
