import copy


class Page:
    def __init__(self, url_prefix, page_num, total_count, params, per_page=10, page_max=11):
        """

        :param page_num: 当前请求页码数
        :param total_count: 数据总行数
        :param url_prefix: 页码标记的页面路径url
        :param per_page: 每页展示数据行数
        :param page_max: 页面上最多显示多少个页码
        """
        self.url_prefix = url_prefix
        self.params = copy.deepcopy(params)


        # 计算总页码
        page_total, m = divmod(total_count, per_page)
        if m:
            page_total += 1
        self.page_total = page_total

        if page_num:
            try:
                page_num = int(page_num)
                if page_num > page_total:
                    page_num = page_total
            except Exception as e:
                page_num = 1
        else:
            page_num = 1
        self.page_num = page_num

        self.per_page = per_page

        if page_max > self.page_total:
            page_max = page_total
        self.page_max = page_max
        page_max_half = self.page_max // 2
        # 计算请求页码切片的起止索引位置
        self.data_start = (self.page_num - 1) * self.per_page
        self.data_end = self.page_num * self.per_page


        page_start = self.page_num - page_max_half
        page_end = self.page_num + page_max_half
        if page_start < 1:
            page_start = 1
            page_end = self.page_max
        if page_end > self.page_total:
            page_end = self.page_total
            page_start = self.page_total - self.page_max + 1
        self.page_start = page_start
        self.page_end = page_end

    @property
    def start(self):
        return self.data_start

    @property
    def end(self):
        return self.data_end

    def page_html(self):
        # 生成页码标签
        li_html_list = []
        # if "page=" in self.url_prefix:
        #     ind = self.url_prefix.find("page=")
        #     self.url_prefix = self.url_prefix[:ind-1]
        # if "/?" in self.url_prefix:
        #     prefix = "{}&".format(self.url_prefix)
        # else:
        #     prefix = "{}?".format(self.url_prefix)

        # 首页
        self.params["page"] = 1
        li_html_list.append('<li><a href="{}?{}">首页</a></li>'.format(self.url_prefix, self.params.urlencode()))
        # 上一页
        if self.page_num > 1:
            self.params["page"] = self.page_num - 1
            li_html_list.append('<li><a href="{}?{}">&laquo;</a></li>'.format(self.url_prefix, self.params.urlencode()))
        else:
            li_html_list.append('<li class="disabled"><a href="#">&laquo;</a></li>')
        # 页码
        for i in range(self.page_start, self.page_end + 1):
            self.params["page"] = i
            # 如果是请求页，就加一个active样式类
            if i == self.page_num:
                li_html = '<li class="active"><a href="{0}?{1}">{2}</a></li>'.format(self.url_prefix, self.params.urlencode(), i)
            else:
                li_html = '<li><a href="{0}?{1}">{2}</a></li>'.format(self.url_prefix, self.params.urlencode(), i)
            li_html_list.append(li_html)
        # 下一页
        if self.page_num < self.page_total:
            self.params["page"] = self.page_num + 1
            li_html_list.append('<li><a href="{}?{}">&raquo;</a></li>'.format(self.url_prefix, self.params.urlencode()))
        else:
            li_html_list.append('<li class="disabled"><a href="#">&raquo;</a></li>')
        # 尾页
        self.params["page"] = self.page_total
        li_html_list.append('<li><a href="{}?{}">尾页</a></li>'.format(self.url_prefix, self.params.urlencode()))
        page_html = "".join(li_html_list)
        return page_html
