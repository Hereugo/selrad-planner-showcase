from . import model_meta

def m2m_create(ModelClass, validated_data):
    info = model_meta.get_field_info(ModelClass)

    many_to_many = {}
    for field_name, relation_info in info.relations.items():
        print(field_name, relation_info.to_many)

        if relation_info.to_many and (field_name in validated_data):
            many_to_many[field_name] = validated_data.pop(field_name)

    instance = ModelClass._default_manager.create(**validated_data)

    if many_to_many:
        for field_name, value in many_to_many.items():
            field = getattr(instance, field_name)
            field.set(value)

    return instance


def m2m_update(instance, validated_data):
    info = model_meta.get_field_info(instance)

    m2m_fields = []
    for attr, value in validated_data.items():
        if attr in info.relations and info.relations[attr].to_many:
            m2m_fields.append((attr, value))
        else:
            setattr(instance, attr, value)

    instance.save()

    for attr, value in m2m_fields:
        field = getattr(instance, attr)
        field.set(value)

    return instance