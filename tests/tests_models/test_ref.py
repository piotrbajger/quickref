from unittest import TestCase

from bibtexmagic.bibtexmagic import BibTexMagic

from quickref import create_app
from quickref.models.ref import Ref
from quickref.models.ref import ref_model_updater
from quickref.forms.ref_edit import RefEditForm


class TestRefModel(TestCase):
    """Tests for the Ref model."""

    def setUp(self):
        self.app = create_app(test=True)
        with self.app.app_context():
            self.form = RefEditForm(
                title="title test",
                author="author test",
                year=2000,
                month=10,
                journal="journal test",
                pages="99--105",
                volume="V",
                number="12",
                editor="editor test",
                publisher="publisher test",
                edition="edition test",
                series="series test",
                address="address test"
            )

        self.test_refs = {
            'article': Ref(
                entry_type='article',
                title='Test Article',
                author='Test McTestface and T. Testovich',
                year=1905,
                month=5,
                journal="International Journal of Testing",
                pages="12-99",
            ),
            'book': Ref(
                entry_type='book',
                title='Test Book',
                author='Test McTestface',
                year=1995,
                editor="Test Editor",
            )
        }

    def test_ref_model_updater(self):
        """Test if refs are updated correctly."""
        entry_types = ['article', 'book']

        for entry_type in entry_types:
            ref_updated = ref_model_updater(self.test_refs[entry_type],
                                            self.form)

            allowed_fields = BibTexMagic.get_fields_for_entry(entry_type,
                                                              optional=True)
            # Cycle through fields allowed for given entry. Verify they were
            # all updated with the form values. Note the special handling of
            # conditionally optional fields.
            for field in allowed_fields:
                if type(field) == str:
                    self.assertEqual(ref_updated.__getattribute__(field),
                                    self.form.__getattribute__(field).data)
                elif type(field) == list:
                    for or_f in field:
                        self.assertEqual(ref_updated.__getattribute__(or_f),
                                        self.form.__getattribute__(or_f).data)

    def test_ref_model_factory(self):
        """TODO: Test that refs are created correctly."""
        pass