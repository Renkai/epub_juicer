from readmdict import MDX, MDD

# https://github.com/ffreemt/readmdict
filename = "resources/etymology/etymonline.mdx"

items = [*MDX(filename).items()]
mdx = {}
for key, val in items:
    # print('key', key)
    mdx[key.decode('utf-8')] = val.decode('utf-8')

etymology = mdx

if __name__ == '__main__':
    print(mdx['unannounced'])
