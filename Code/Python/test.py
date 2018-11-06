from NeuralNetwork import *
import datetime as datetime
nn = NeuralNetwork(11,1)

nn.setWeights([-0.99639, -0.954398, -0.18814, -0.873413, -0.211008, 0.35114, -0.553564, -0.096986, -0.447506, -0.945995, -0.086601, -0.619426, -0.913524, -0.775755, -0.981632, -0.977238, -0.550635, -0.604988, -0.816707, -0.983051, -0.975626, -0.870962, -0.861339, -0.900366, -0.965061, -0.815547, -0.943636, -0.977468, -0.950746, -0.98822, 0.679052, 0.732704, 0.99983, 0.617737, -0.066434, -0.536102, -0.265036, -0.690879, -0.524027, 0.05221, -0.060823, 0.039311, -0.554001, 0.03851, 0.29264])
T0 = 23
T2 = 19
T0 = (T0-20.995)/(35.515-20.995)
T2 = (T2-23.545)/(29-357-23.545)
now = datetime.datetime.now()
midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
secondsPastMidnight = float((now - midnight).seconds)/86400.0
nn.predict([T0, T2, secondsPastMidnight])

print (nn.predict([T0, T2, secondsPastMidnight])*(28.981-24.372)+24.372)