from cognitive.format.basicelements.concepts.concept_base_classes import IRegisterable


class RegisteredItem(IRegisterable):
    def get_uuid(cls) -> bytearray:
        pass

    def get_timestamp(cls) -> int:
        pass

    def register(cls, domain: IRegisterable):
        pass


def main():
    i = RegisteredItem()
    i2 = RegisteredItem()
    i.register(i2)


if __name__=="__main__":
    main()