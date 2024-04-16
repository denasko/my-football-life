import folium

my_map = folium.Map(location=[53.898774518559485, 27.558347479207473],zoom_start=20)

tootlip = 'Поле гимназии №25'

folium.Marker([53.868415729778704, 27.659269292148736], popup="Поле гимназии 25").add_to(my_map)

my_map.save('/home/den/PycharmProjects/my-football-life/events/templates/map/my_map.html')
