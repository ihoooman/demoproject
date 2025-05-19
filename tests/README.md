# Tests

This directory contains tests for the LastDjangoProject.

## Structure

- `test_accounts.py`: Tests for the accounts app
- `test_dashboard.py`: Tests for the dashboard app

## Running Tests

You can run the tests using Django's test runner:

```bash
python manage.py test tests
```

Or using pytest:

```bash
pytest tests/
```

## Adding New Tests

To add new tests:

1. Create a new file in the tests directory with a name starting with `test_`
2. Import the necessary Django test classes and models
3. Create test classes that inherit from `django.test.TestCase`
4. Add test methods that start with `test_`

Example:

```python
from django.test import TestCase
from myapp.models import MyModel

class MyModelTest(TestCase):
    def setUp(self):
        self.my_model = MyModel.objects.create(name='Test')
    
    def test_my_model_creation(self):
        self.assertEqual(self.my_model.name, 'Test')
```