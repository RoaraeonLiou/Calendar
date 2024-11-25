from generators.generator import GeneratorMeta

if __name__ == "__main__":
    # test
    print(GeneratorMeta.registry)
    for class_name in GeneratorMeta.registry:
        generator = GeneratorMeta.registry.get(class_name)()
        generator.parse(f"config/{generator.generator_name}.json")
        generator.generate(f"ics/{generator.generator_name}.ics")

