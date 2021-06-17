# build network, define training details

from keras.models import Model
from keras.layers import Dense, Input, Flatten, concatenate
from keras.applications.densenet import DenseNet121
from keras.optimizers import Adam


def build_network(img_height, img_width, top_ingredient_number):
    
    base_model = DenseNet121(weights='imagenet', include_top=False, input_shape=(img_width, img_height, 3))
    base_model.trainable = False

    x = base_model.output
    x = Flatten()(x)
    x = Dense(128, activation='relu')(x)

    nutrient_pred = Dense(8, name='nutrients')(x)
    ingre_pred = Dense(top_ingredient_number, activation = "sigmoid", name='ingredients')(x)

    # out = concatenate([nutrient_pred, ingre_pred])

    model = Model(inputs=base_model.input, outputs=[nutrient_pred, ingre_pred])
    # model.summary()
    
    return model


def train_network(normalized_imgs, nutrient_information, ingre_vectors, img_height, img_width, top_ingredient_number, epoch):
    
    model = build_network(img_height, img_width, top_ingredient_number)
    model.compile(optimizer=Adam(lr=1e-4), loss={'nutrients':'mse', 'ingredients':'binary_crossentropy'}, 
                  metrics=['accuracy'])
    history = model.fit(normalized_imgs, [nutrient_information, ingre_vectors], 
              validation_split=0.2, epochs=epoch, verbose=1, batch_size=1)
    
    return model, history











