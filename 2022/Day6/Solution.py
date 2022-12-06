##### Day 6 #####
# https://adventofcode.com/2022/day/6

# ------------------------------------------------
# imports
# ------------------------------------------------
import numpy as np

# ------------------------------------------------
# read and prepare input
# ------------------------------------------------
datastreams = [
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
]
datastream_orig = "jfnjjwbbqttplpvllqgllmdllfmllscssqmqzmmwzznqnwqnwnqnjjbdbpbtbdbzzzljljzjjpccrmmppzfpzfpfnfccfbbcqcrcffblfbftbfbtbwwwmgwmgmnngnllnfllhghcghhjppchcfcnfffllmmqbmmpwwwwlqwwqgqcqsqjqpqzqqdzdtztltslsljjfqfcqqgbqqqghqgqvgvrggqwggrgjgmmnrmmzgmzgzpzjjctcmtcmcnndppcvpvrrwvrvhrvhrhjhnjnvjnjrjggccvffnqqvfqvvnmvmqmfmfqqzfzbfzzzgpzpllrwwnpwpnwnwgwhhrrdnrrdjjzjszsjjbddcdbbvmbmqbqnbqbsqbsqqwbwhwggssdnnmttvnnvmnmhmfhhjchcttzdzdqqszzcwwhhwzhwhphqhcqqsggddfmmvzmzwmwfwzwrrbmrrnwnfnwnlwnwrwfwnnmtnnzwnwdnnbhhrphrhlhwllpmmbcbtbffmqffddjnjwwzpzfpptbbqqwbwzbzjbjmjljblbtlblqqhqbqggrngrgllbmbccmhmqmqwwqcqssqzzfjzjrjnnqrqssfnsnvvtgvvmsvsqqljjbsbrrjllvfvzfzmzhzzhthjhshlslfljfjqjpqpvvmpmhpmhmqqmmdwmddppjlplhlsstlssgnggrbblggffcdfdzzwqqtztqtwqtwtzzsjsbszsbsvbvwwjqjnnpdpccwssvdsdzzqbqbtbtqtmtltltvlvddzwzzfpzpjpgphprpgpqqwppdwpdplddvffcdffvpvqqgvqgvvrfvrvqrrcjcpjjpttftqqvjqvqsvqsvqssdpdbbbmcmscsddbhhgttwhhjlltqllnqntqtsscnntwwhswswlwggldltlttsjszsnznsznzccbtbblplnnmfmqmrrvjvhjhzhnzzgnnhrrdrllblpbllfdfjjssvnssvlsllnqqhwqhhhsgstsjstthrrhrghrhhfmhmwhwrwwsrwrfwwdnntqnnsvnvmnnfvnntztqzqhqnqjnnjfflbfllrsllqhqdqccgvgnvvcwcfccmssqnqhhqrrfrtrvvnjnpjnjjpplmlppvmpphjhppvhvdvssjcjrrtrdrrsvvbbjzzrtztgzghzhccwmccshhzbhhdwdwsdswwlcwllpblpphrppfhfnffrbbcgcmggnvnzzmvvcrrftrftrffcscvcsslbljlglzgzbzczszmsmbmnbbhdhvvsqvqhvvfrfddbpwgvztwwqcpzhhwnhphnrwldjmztsptbbgsqbqqccwbdqzvhfjlfldgphzbfprclgpfztbrgvsvfpghmdchscbdqjqgzvmrtdrfzbhgdvgznjcsmglcfwhdtpsljnvvzjcbbrczwtgpdmgpzhctvbbmvsjzthffsjqhfsdrclpqslbhnmpczwvggpzbjcchfjzjhhgtrmlgnzlndfvzrccgggrpmprbmjbfjjhzrhrtwgqdbgdlqghssrnmtmpvttcqwnwdzhgfnddgbqcsdvzvwqdnmmpwrwhfbqtcpqhvwbczrmjqzsntvdrncwjsmvvwcngrtlwtjmnctwrrtvphbjhlqmgzfsfsrblzzvmzlbhzjhwbdfpncdrfchmrqhspdszcjrnvwtmjzmsmzcdphsdzjgqswwrpdvlpvrdnhplnlmswvcrzlcmbtqtscjfwrnrctrvdqcqzwcvgvpdgrndrgsrvzftwpqjjgjhzwhvrjlqntdtcjdrqzhqlqqdffcgvttlhvwgggnwmdlvghfgjpsmntbvbjbbttrwsljwsrvtmznvqdptpwtdcwtcsfdjlmdqthqggjcptrqhbsbjzqqmvvjmgmppqmjmnjdqvspzlbgzjsjshpslmszqnzghsszpsmpzfcrqqjdwvtbnzstvvjzvtzgpptcmvmbvmpvpzvgfnwtlmdzhvhshtwvnbgwmtzqhcptflpqsqvmptchpfcbwhvjzdcnsnqrgdwfcthqfssnbqnvgvvhlzqfqmdlcwnshtvhhhpghjbmhdbfbqcvbnbvwbzcbbmjnrqmsdqnmnbsrvhggzsrlbwtfmgwrnlhrbrrrqdcspnrpnppngrtdqtbmbhcbjrlhpfjpdnfndmqvwvhlgmsntpwrlrwwqhwvzbpzqqggnbqlsjjqtbqjcdpmndgmtdhfbqrpdzzsnmhzmqqnbdqftqmnhfbdzdlfwgjsjhrcsmtfzgwbvbbzdrlbmcgmppqfppmbqrnsmrmhrdsvgcfmzpfnvrbbgfccfcbphszwdbnnwcjjvvlpdtfzgtslvgqwmsvlpzjcbqwqclrjrsgthhtqrqrhvsdfjntgllsvslrvdtnsdmrgtqcmswnqwlrwlfmcfftbjpvdnmczqzldsssszhjtqtqvqtwhjcqchjvqvntvzzzprbmjcctsqfdcvpbtsgnnsqtqnmjhrgqcjnzrdsgrbtdpqjbgcmnfwhnsrfwcdmncjzwcngfbmmrsbvgvvqpvrdjfsqwjdmqjdpzcbjjfmzjjgbnwqgrvpmbzdhsgtldrzvglscfwbmjltcrzrgdslgprwscwbrhtdtglznjdcvfjzjjqzntdqdbcrcbbmvnzdshjzcsfsgpghmgdqdwsnwjtvtbqbqccbcwjpnhdhzcvdssvnvqtvzwprhpgftdwwvgsbnlzzjppcrrwmrsthvjjrvrsdrbdqfgsjsmwfplpstrbnpdhhcblhjfwzngmhlwbvnfcbgwshspsbbgbldrvmcnczszpgnddrfwrtgcqjggrrcbjwrdjlrvtspbftrtjbzjwchpfnjctcjtwtpmtblczcftqlphdjczfrvtzlsglpvhqsqqblttdjrlczhrqsgpggmvnhpqtrfbpgvzftwtsmwhwswtpvtwnsshmlcffpcjshqhqqsjtpbgszscmcbnhjjtjmpgfdhgmljqmmwlfptstjjvqhcbjpjpwzwqflhslclzzjlmcttbsncqmfzhgnzwbdtnvfwbtztwbhtfsqjfzwmfflmbwnqzqhcjwdpbvngsgzlwvwcqhqjsndznbbdcqqhmjjpqjbsnvwztgmqwdcbbjvcndmhsbvbjnzlbscmgnjcrrwrfdljtcsgmwtffgcjflpzzdcnzvmrbnrjbbmhzqqjtgsrwqmmrhpndwlbnrtrhhpqlmdrcrtdmzsslrmffpftdjvfcpvvhzhjhqtrrsclvtbsccgmmqrjbqgbmpnbzlsncssdhmjppjptvddfgbbnjzjjldjlqjzhhttsclrmsgzctwjqqvtjlfzwgtffgrdjzwdcnrprlcswffghngrqcgsbzqhhvbfjtwcjlrrmbtqjdrgpnbftnmzqnndnqwgrqndlwmjnnspbhjlnzrnptnrmcjhpbfcqpvbchvdwthjlcrfpssgtfbsgfrftcrwttrspbsvzpvcczmdqslcdgfljvtjsdpjnwmdvfzfllrdrbgvpltzlqcrlwbncswhfvrdthspmhfhfdlvpbcqlmjfznhnqblffftgzqrtswnmtnvjprqqhhhvrscvbbzgmnlnprghfdjqbgjppjzjrnclfdssbmgspwcscnlcrrqmtlljrmcwgdgcqwvvjzvsjdjvsspszlcthwzrwqtzdgmqvnlvvzrvrpqqwswzcchncrpnjdmflvmhhwvrrstpvnszfrmvpdtpqpbdmwvvbbpjnwmtststtlcvqdnvqqphzlhhzbbbjssgdcnhlmwrzwvwmcmgrcngqzcnffqzfnvldpdjmsspgpbrzhnszfnljfcrgsjvqjjbstvghlcslhqlzhltpglwffrzfgjghssfgrptbnpbhqnhhfbjsnmsvltqpthdmzzrhrhhmzlplvrtdqfrfrppdpqnllblcfjqpdwznsbrhcncdpmztcrjrfnlwtznrmpbzqsbrqrbnthgfpshrdhnwjmrnsmsfqwdjsmsvhfrbdpjrwcvmdvvmdtfqjgmdsrqtctsdmznngbsrfjvhllgwt"
# ------------------------------------------------
# Solution
# ------------------------------------------------
def get_start_of_pack_maker(datastream, size):
    # bag of words [letters] of the size
    bow = np.lib.stride_tricks.sliding_window_view(list(datastream), size)
    return np.where([len(np.unique(x)) == size for x in bow])[0][0] + size


# ---------------- part 1 ----------------
for datastream in datastreams:
    print(datastream)
    print(get_start_of_pack_maker(datastream, 4))
get_start_of_pack_maker(datastream_orig, 4)

# ---------------- part 2 ----------------
for datastream in datastreams:
    print(datastream)
    print(get_start_of_pack_maker(datastream, 14))
get_start_of_pack_maker(datastream_orig, 14)
