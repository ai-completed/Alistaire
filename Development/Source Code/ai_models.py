import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, GRU, Bidirectional, Regularization
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_error
import numpy as np
import matplotlib.pyplot as plt

class EnhancedTimeSeriesPredictor:
    def __init__(self, input_shape, output_shape, model_type='LSTM', layers=2, units=50, dropout=0.2, regularization_lambda=0.01):
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.model_type = model_type
        self.layers = layers
        self.units = units
        self.dropout = dropout
        self.regularization_lambda = regularization_lambda
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        for i in range(self.layers):
            return_sequences = True if i < self.layers - 1 else False
            if self.model_type == 'LSTM':
                model.add(LSTM(self.units, return_sequences=return_sequences, input_shape=(self.input_shape, 1),
                               kernel_regularizer=Regularization.l2(self.regularization_lambda)))
            elif self.model_type == 'GRU':
                model.add(GRU(self.units, return_sequences=return_sequences, input_shape=(self.input_shape, 1),
                              kernel_regularizer=Regularization.l2(self.regularization_lambda)))
            else:
                raise ValueError('Unsupported model type. Choose either LSTM or GRU.')
            model.add(Dropout(self.dropout))

        model.add(Dense(self.units, activation='relu'))
        model.add(Dense(self.output_shape))
        model.compile(optimizer='adam', loss='mse')
        return model

    def train(self, X_train, y_train, epochs=100, batch_size=32, validation_split=0.1):
        early_stopping = EarlyStopping(monitor='val_loss', patience=10, mode='min', restore_best_weights=True)
        history = self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=validation_split, callbacks=[early_stopping])
        return history

    def evaluate(self, X_test, y_test):
        predictions = self.model.predict(X_test)
        mse = mean_squared_error(y_test, predictions)
        mae = mean_absolute_error(y_test, predictions)
        return mse, mae

    def plot_history(self, history):
        plt.plot(history.history['loss'], label='train')
        plt.plot(history.history['val_loss'], label='test')
        plt.legend()
        plt.show()

if __name__ == '__main__':
    # Mock-up example for data preparation and feature engineering
    # Assume 'data' is a loaded time-series dataset
    
    from sklearn.preprocessing import MinMaxScaler
    import numpy as np
    
    # Example data loading
    # data = load_your_time_series_data_here()
    data = np.random.randn(1000)  # Mock data, replace with actual data loading
    data = data.reshape(-1, 1)  # Reshape data to fit MinMaxScaler requirements
    
    # Normalize the data
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    
    # Feature Engineering: Create time steps for LSTM/GRU
    def create_time_steps(data, steps=1):
        X, y = [], []
        for i in range(len(data) - steps - 1):
            a = data[i:(i + steps), 0]
            X.append(a)
            y.append(data[i + steps, 0])
        return np.array(X), np.array(y)
    
    time_steps = 100  # Number of steps you're considering at a time
    X, y = create_time_steps(scaled_data, steps=time_steps)
    
    # Reshape X for LSTM/GRU input
    X = X.reshape(X.shape[0], X.shape[1], 1)
    
    # Split the data into training and testing
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize the model
    input_shape = X_train.shape[1]
    output_shape = 1  # Predicting a single value
    predictor = AdvancedTimeSeriesPredictor(input_shape, output_shape, model_type='LSTM')
    
    # Train the model
    predictor.train(X_train, y_train)
    
    # Evaluate the model
    predictions = predictor.predict(X_test)
    # Here you would compare 'predictions' with 'y_test' using your preferred evaluation metrics
    
    print("Model training and evaluation complete.")
  
    print("Enhanced AI Model ready for advanced operations.")
