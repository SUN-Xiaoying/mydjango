# Activate the virtual environment
source venv/bin/activate

# Install Django
pip install django

# Create a new Django project
django-admin startproject myproject

# Navigate into the project directory and run the development server
```bash
cd myproject
python manage.py runserver
```

# Start APP

```bash
python manage.py startapp myapp
```


When run the OcppSimulator locally, we sometimes get error.
```bash
org.springframework.beans.factory.BeanCreationException: Error creating bean with name 'org.springframework.boot.context.properties.ConfigurationPropertiesBindingPostProcessor': Invocation of init method failed; nested exception is java.lang.NoClassDefFoundError: javax/xml/bind/ValidationException
        at org.springframework.beans.factory.support.AbstractAutowireCapableBeanFactory.initializeBean(AbstractAutowireCapableBeanFactory.java:1578)
        at org.springframework.beans.factory.support.
        ...
```

To solve this, 

1. Download jdk version 1.8 and add its path to `venv/bin/activate`.


```bash
PATH="$VIRTUAL_ENV/bin:$HOME/.sdkman/candidates/java/8.0.392-amzn/bin:$PATH"
export PATH
```

2. restart venv

```bash
source deactivate
source venv/bin/activate
```