#############################################################
# FILE: ex10.py
# WRITER: Keren Meron, keren.meron, 200039626
# EXERCISE: intro2cs ex10 2015-2016
# DESCRIPTION: mapping of articles in a wikipedia network
#############################################################

def read_article_links(file_name):
    '''
    Returns all pairs of articles in a file, as a list of tuples, each
    tuple representing a pair.
    param file_name(str): name of file to read from.
    '''

    file = open(file_name, 'r')
    content = file.read()
    lines_in_file = content.splitlines()
    pairs_in_file = [tuple(line.split()) for line in lines_in_file]

    return pairs_in_file


class Article():
    '''
    This class holds all information for the Article object.
    An Article has attributes of a name, rank and a collection, which holds
    all instances of Article which are neighbors to current Article.
    '''

    INIT_RANK = 1

    def __init__(self, name):
        '''
        Initializes all of the containers needed for this class to work.
        attr name(str): name of the article
        attr collection(set): contains all neighbors (type Article) of the
                    article, meaning those which the article has links to.
        attr rank(float): article's rank, will be calculated by pagerank alg
        '''

        self.__name = name
        self.__collection = set()
        self.__rank = self.INIT_RANK


    def update_rank(self, amount, add=False):
        '''
        Sets article's rank.
        param amount(float): amount to set/add to current rank.
        param add(bool): wheter to add or set the amount given.
        '''

        if add:
            self.__rank += amount
        else:
            self.__rank = amount

    def get_rank(self):
        '''Return Article's rank.'''
        return self.__rank

    def get_name(self):
        '''Returns the name of the article, as a string.'''
        return self.__name

    def add_neighbor(self, neighbor):
        '''Adds an instance of neighbor (type Article) to the collection.'''
        self.__collection.add(neighbor)

    def get_neighbors(self):
        '''Returns a list of objects which are neighbors of the article.'''
        return list(self.__collection)

    def __len__(self):
        '''Returns the number of neighbors the article object has.'''
        return len(self.__collection)

    def __contains__(self, article):
        '''
        Returns True if the article (in parameter) is a neighbor of the
        current article, otherwise False.
        param article(Article): an instance of Article
        '''

        if article in self.__collection:
            return True
        else:
            return False

    def __repr__(self):
        '''
        Returns a string representation of the Article object.
        Contains the object's name, and a list of its neighbors' names.
        '''

        neighbors_names = [i.get_name() for i in self.__collection]
        return str((self.__name, neighbors_names))


class WikiNetwork():
    '''This class holds all information for the WikiNetwork object.'''

    INIT_MONEY = 0.9
    INIT_JAC_IDX = 1

    def __init__(self, link_list=[]):
        '''
        Initializes all of the containers needed for this class to work.
        attr link_list(list): list of article pairs, each pair being an
                article and its neighbor, as returned by read_article_links().
        attr collection(dict): a collection of all articles.
                key: name(str) of Article
                value: list of names of Articles which are neighbors to key
        attr articles(dict): another collection of all articles.
                key: string of article
                val: instance of the article
        '''

        self.__link_list = link_list
        self.__collection = {}
        self.update_network(link_list)

    def update_network(self, link_list):
        '''
        Creates an Article object for each article appearing in link_list.
        Adds Articles and their names to the articles dictionary.
        Adds all article pairs to the collection dictionary of current object.
        param link_list(list): list of article pairs, each pair being an
                article and its neighbor, as returned by read_article_links().
        '''

        for pair in link_list:

            temp0 = self.create_article_helper(pair, 0)
            temp1 = self.create_article_helper(pair, 1)

            if temp1 not in temp0.get_neighbors():
                temp0.add_neighbor(temp1)

    def create_article_helper(self, pair, index):
        '''
        Checks if the article exists, and if not creates an instance of it,
        and adds to the collection dictionary (of all articles in network).
        param pair(tuple): contains an article name and its neighbor's name.
        param index(int): index of pair, specifies if first or second name.
        Returns the instance of the article handled.
        '''

        if pair[index] not in self.__collection:
            temp = Article(pair[index])
            self.__collection[pair[index]] = temp
        else:
            temp = self.__collection[pair[index]]

        return temp


    def get_articles(self):
        '''Return a list of all Articles in the WikiNetwork.'''
        return list(self.__collection.values())

    def get_titles(self):
        '''Return a list of all Article names (strings) in the WikiNetwork.'''
        return list(self.__collection.keys())

    def __contains__(self, article_name):
        '''
        Returns True if the WikiNetwork contains an instance of article_name,
        otherwise returns False.
        param article_name(str): the name of an Article object.
        '''

        if article_name in self.get_titles():
            return True
        else:
            return False

    def __len__(self):
        '''Returns the number of Article objects in the WikiNetwork.'''
        return len(self.__collection)

    def __repr__(self):
        '''
        Returns a string representation of the WikiNetwork, which will
        represent a dictionary whose keys are article names, and values are
        Article instances.
        '''

        return str(self.__collection)

    def __getitem__(self, article_name):
        '''
        Return the Article instance of given name.
        If the article does not exist in network, raises KeyError exception.
        param article_name(str): name of wanted article.
        '''

        if article_name in self.__collection:
            return self.__collection[article_name]
        else:
            raise KeyError(article_name)


    def page_rank(self, iters, d= INIT_MONEY):
        '''
        Sorts the articles using Google's page rank algorithm.
        Algorithm gives points proportional to amount of pointers (from
        other articles) to an article.
        In an iteration, each article will give each of its neighbors points
        according to its own point rank.
        Return list of all pages, in order of highest rank to lowest.
        If some pages with the same rank, will return in lexical order.
        param iters(int): number of times to preform algorithm's iteration.
        param d(float): amount of points each article starts with.
        '''

        i = 0
        while i < iters:
            self.page_rank_iteration(d)
            i += 1

        ranks_sorted = sorted(self.get_titles(), key = lambda
                    article : (-self[article].get_rank(), article))

        return ranks_sorted


    def page_rank_iteration(self, d):
        '''
        One iteration calculating and returning the page rank.
        Ranking calculation algorithm:
        Each article divides equally to each of its neighbors an amount equal
        to its current page rank times d. At the end of the round, each
        article will have the amount received from all other articles pointing
        at him, plus (1-d).
        param d(float): const, amount to divide up at beginning of iteration.
        '''

        temp_ranks = dict()

        self.calculate_ranks_helper(temp_ranks, d)

        for article in self.get_articles():
            article.update_rank(1-d)
            if article in temp_ranks:
                article.update_rank(temp_ranks[article], True)

    def calculate_ranks_helper(self, temp_ranks, d):
        '''
        Calculates and updates in temp_ranks dictionary the points which
        the article will give to each of its neighbors.
        param article(Article): the article which is giving out points.
        param temp_ranks(dict): dictionary which holds for each article,
                    the points it will receive at the end of the round.
        param d (float): constant by which to calculate amount of points.
        '''

        for article in self.get_articles():
            if len(article):
                amount_given = (article.get_rank() * d) / len(article)

            for neighbor in article.get_neighbors():
                if neighbor not in temp_ranks:
                    temp_ranks[neighbor] = amount_given
                else:
                    temp_ranks[neighbor] += amount_given


    def jaccard_index(self, article_name):
        '''
        Returns a list of all articles (type Article) in the network,
        sorted by their jaccard index, and if similar then by lexical order.
        param article_name(str): name or Article in relation to which the
                                jaccard index is computed
        '''

        if article_name not in self.get_titles():
            return None

        neighbors = self[article_name].get_neighbors()
        jac_indexes = {}

        if not neighbors:
            return None

        self.calculate_jaccard(jac_indexes, neighbors, article_name)
        jac_sorted = sorted(jac_indexes, key = lambda a: (-jac_indexes[a], a))

        return jac_sorted


    def calculate_jaccard(self, jac_dict, neighbors, article_name):
        '''
        Calculates the Jaccard index of each article in the network.
        calculated by the number of objects in the intersection of two
        articles' neighbors, divided by the union of those two.
        param jac_dict(dict): contains an article(key) and its index.
        param neighbors(lst): contains all neighbors (Article) of an article.
        param article_name(str): name of Article.
        '''

        for other_article_name in self.__collection:
            if other_article_name == article_name:
                jac_index = self.INIT_JAC_IDX
            else:
                neigh_set = set(neighbors)
                other_neigh = set(self[other_article_name].get_neighbors())

                intersection = len(neigh_set & other_neigh)
                union = len(neigh_set | other_neigh)
                jac_index = intersection / union

            jac_dict[other_article_name] = jac_index


    def travel_path_iterator(self, article_name):
        '''
        Returns an iterator which returns by order the names of the articles
        which were in the path of article_name.
        The iterator travels goes to an article's neighbor, choosing the
        article which is neighbor to most others (and if several, then by
        lexical order).
        If article_name doesn't exist, or article doesn't have neighbors,
        will raise StopIteration Exception.
        param article_name(str): name of an Article object.
        '''

        travel_iterator = iter(self.travel_path(article_name))
        return travel_iterator

    def travel_path(self, article_name):
        '''
        Yields a list of article names, each name is in path of previous.
        Path is chosen according to which neighbor of an article is the
        neighbor to most articles in total.
        param article_name(str): name of an Article object.
        '''

        if article_name not in self.get_titles():
            return

        step = article_name
        while True:
            yield step
            if not len(self[step]):
                raise StopIteration
            step = self.travel_one(step)


    def travel_one(self, article_name):
        '''
        Returns the neighbor of article_name which is the neighbor to most
        other articles. If several with same amount, returns in lexical order.
        param article_name(str): represents the name of an article.
        '''

        sorted_pointers = self.appoint_sort_pointers(self[article_name])
        next_article = sorted_pointers[0]

        return next_article.get_name()


    def appoint_sort_pointers(self, article):
        '''
        Returns a list of Articles, sorted numerically by the number of
        pointers they each have, and if similar, then in lexical order.
        Pointers - how many articles have a neighbor of article as their own.
        param article(Article): the article for which to check neighbors.
        '''

        neighbor_pointers = {}

        for neighbor in article.get_neighbors():
            for pointer in self.get_articles():
                if neighbor in pointer.get_neighbors():
                    if neighbor in neighbor_pointers:
                        neighbor_pointers[neighbor] += 1
                    else:
                        neighbor_pointers[neighbor] = 1

        sorted_pointers = sorted(neighbor_pointers, key = lambda
                                n : (-neighbor_pointers[n], n.get_name()))

        return sorted_pointers


    def friends_by_depth(self, article_name, depth):
        '''
        Returns a list of articles which are reachable from article_name by
        depth number of legal moves. A legal move is from an article to one
        of its neighbors.
        param article_name(str): represents an Article object.
        param depth(int): number of moves.
        '''

        if article_name not in self.get_titles():
            return None

        friends = set()
        friends.add(article_name)
        friends = self.friends_helper(self[article_name], depth, friends)
        return list(friends)

    def friends_helper(self, article, depth, friends):
        '''
        Returns a list of articles which are reachable from article_name by
        depth number of legal moves. A legal move is from an article to one
        of its neighbors.
        param article(Article): represents an Article object.
        param depth(int): number of moves.
        param friends(set): contains and will be updated with all articles
                            which the article can reach with depth.
        '''

        if not depth:
            friends.add(article.get_name())
            return friends

        for neighbor in article.get_neighbors():
            self.friends_helper(neighbor, depth-1, friends)
            friends.add(article.get_name())

        return friends
