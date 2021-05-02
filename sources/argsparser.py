
import argparse


def get_arguments():
    """
    Parses the argparse object
    :returns the arguments object
    """
    parser = argparse.ArgumentParser(description='', epilog="")
    parser.add_argument('title', help='Movie title', default=None)
    parser.add_argument('-l',"--lang", help='language of the streaming', default="fr")
    args = parser.parse_args()
    return args
