import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit


def turn_to_num(value):
    try:
        return int(value)
    except:
        return 0


class ExtrafieldsIDatasetFormPlugin(plugins.SingletonPlugin, toolkit.DefaultDatasetForm):
    plugins.implements(plugins.IDatasetForm)
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IValidators)

    # IValidators

    def get_validators(self):
        return {
            u'turn_to_num': turn_to_num,
        }

    # IDatasetForm

    def _create_vocabulary(self, name, values):
        user = toolkit.get_action('get_site_user')({'ignore_auth': True}, {})
        context = {'user': user['name']}
        try:
            data = {'id': name}
            toolkit.get_action('vocabulary_show')(context, data)
        except toolkit.ObjectNotFound:
            data = {'name': name}
            vocab = toolkit.get_action('vocabulary_create')(context, data)
            for tag in values:
                data = {'name': tag, 'vocabulary_id': vocab['id']}
                toolkit.get_action('tag_create')(context, data)

    def create_culture_medium(self):
        self._create_vocabulary('culture_medium', (u'Maintenance', u'EBM2'))

    def create_toxin(self):
        self._create_vocabulary('toxin', (u'Dox', u'Ami', u'TBBPA', u'Blank'))
    
    def create_age_type(self):
        self._create_vocabulary('age_type', (u'Old', u'Young'))
    
    def create_dimension(self):
        self._create_vocabulary('dimension', (u'2D', u'3D'))

    def create_category(self):
        self._create_vocabulary('category', (u'Metabolomics', u'Proteomics', u'Transcriptomics', u'Toxin targeted metabolomics', u'Chip sensors', u'In vitro assays'))
    
    def create_content(self):
        self._create_vocabulary('content', (u'Cells', u'Culture media', u'Not applicable'))

    def create_model(self):
        self._create_vocabulary('model', (u'Static', u'Dynamic'))
    
    def _tag_list(self, name):
        try:
            tag_list = toolkit.get_action('tag_list')
            toxin = tag_list(data_dict={'vocabulary_id': name})
            return toxin
        except toolkit.ObjectNotFound:
            return None

    def culture_medium(self):
        self.create_culture_medium()
        culture_medium = self._tag_list('culture_medium')
        return culture_medium

    def toxin(self):
        self.create_toxin()
        toxin = self._tag_list('toxin')
        return toxin
    
    def age_type(self):
        self.create_age_type()
        age_type = self._tag_list('age_type')
        return age_type
    
    def dimension(self):
        self.create_dimension()
        dimension = self._tag_list('dimension')
        return dimension

    def category(self):
        self.create_category()
        category = self._tag_list('category')
        return category

    def content(self):
        self.create_content()
        content = self._tag_list('content')
        return content

    def model(self):
        self.create_model()
        model = self._tag_list('model')
        return model

    def _modify_package_schema(self, schema):
        schema.update({
            'size': [
                toolkit.get_validator('turn_to_num'),
                toolkit.get_converter('convert_to_extras')
            ]
        })
        schema.update({
            'culture_medium': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_tags')('culture_medium')
            ]
        })
        schema.update({
            'replicates_number': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'cells_number': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'ratio_hipsccms_hcaecs': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'experiment_date': [toolkit.get_validator('ignore_missing'),
                            toolkit.get_converter('convert_to_extras')]
        })
        schema.update({
            'toxin': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_tags')('toxin')
            ]
        })
        schema.update({
            'age_type': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_tags')('age_type')
            ]
        })
        schema.update({
            'dimension': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_tags')('dimension')
            ]
        })
        schema.update({
            'category': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_tags')('category')
            ]
        })
        schema.update({
            'content': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_tags')('content')
            ]
        })
        schema.update({
            'model': [
                toolkit.get_validator('ignore_missing'),
                toolkit.get_converter('convert_to_tags')('model')
            ]
        })

        return schema

    def create_package_schema(self):
        schema = super(ExtrafieldsIDatasetFormPlugin, self).create_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(ExtrafieldsIDatasetFormPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(ExtrafieldsIDatasetFormPlugin, self).show_package_schema()
        schema.update({
            'size': [
                toolkit.get_converter('convert_from_extras'),
                toolkit.get_validator('turn_to_num')
            ]
        })
        schema.update({
            'culture_medium': [
                toolkit.get_converter('convert_from_tags')('culture_medium'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'replicates_number': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'cells_number': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'ratio_hipsccms_hcaecs': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'experiment_date': [toolkit.get_converter('convert_from_extras'),
                            toolkit.get_validator('ignore_missing')]
        })
        schema['tags']['__extras'].append(toolkit.get_converter('free_tags_only'))
        schema.update({
            'toxin': [
                toolkit.get_converter('convert_from_tags')('toxin'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'age_type': [
                toolkit.get_converter('convert_from_tags')('age_type'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'dimension': [
                toolkit.get_converter('convert_from_tags')('dimension'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'category': [
                toolkit.get_converter('convert_from_tags')('category'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'content': [
                toolkit.get_converter('convert_from_tags')('content'),
                toolkit.get_validator('ignore_missing')]
        })
        schema.update({
            'model': [
                toolkit.get_converter('convert_from_tags')('model'),
                toolkit.get_validator('ignore_missing')]
        })

        return schema
    
    def is_fallback(self):
        return True

    def package_types(self):
        return []


    # IConfigurer

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')


    # ITemplateHelpers

    def get_helpers(self):
        return {
            'culture_medium': self.culture_medium,
            'toxin': self.toxin,
            'age_type': self.age_type,
            'dimension': self.dimension,
            'category': self.category,
            'content': self.content,
            'model': self.model
        }