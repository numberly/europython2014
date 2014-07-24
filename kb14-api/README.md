kb14 API
========

Before running
--------------

* Make sure you got `gevent`, `flask` and `mongoengine`, and make sure you're running
it under uWSGI (see `kb14-api.ini.example` for an example uWSGI config).

* Rename `config.py.example` as `config.py` and edit it if your MongoDB server
is not on the same machine.


Keyboard methods
----------------

#### **GET** /keyboards

Get all registered keyboards.


#### **GET** /keyboard/[keyboard_color]

Get a given keyboard.


#### **GET** /keyboard/[keyboard_color]/keys

Get all keys pressed by a given keyboard.


#### **GET** /keyboard/[keyboard_color]/key/[key_name]

Get all keys pressed for a given keyboard and a given key.


#### **POST** /keyboard

Register a new keyboard.
* **Arguments:**
	* `color` (required)


#### **POST** keyboard/[keyboard_color]/key

Register a key pressed by a keyboard.
* **Arguments:**
	* `name` (required)


Key methods
-----------

#### **GET** /keys

Get all pressed keys.


#### **GET** /key/[key_name]

Get all pressed keys for this key.
