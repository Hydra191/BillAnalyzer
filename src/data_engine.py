import pandas as pd

class DataEngine:
    def __init__(self):
        self.raw_data = None
        self.target_column = '金额(元)'

    def process_alipay_bill(self, file_path):
        """读取并处理支付宝账单"""
        try:
            # 1. 读取原始数据
            df = pd.read_csv(file_path, skiprows=24,encoding='gbk')
            column_mapping = {
            '金额': '金额(元)',
            }
            df = df.rename(columns=column_mapping)
            # 2. 预清洗：确保金额是数字类型
            # 这一步非常重要，解决了你之前提到的排序不正常问题
            df[self.target_column] = pd.to_numeric(
                df[self.target_column].astype(str).str.replace('¥', ''), 
                errors='coerce'
            )

            # 3. 筛选需要的列
            keep_columns = ['交易时间', '交易对方', '商品说明', '收/支', self.target_column]
            df = df[keep_columns].dropna(subset=[self.target_column])
            df = df[df['收/支'] != '不计收支']

            # 4. 执行多级排序：商家(A-Z) -> 金额(大到小) -> 时间(新到旧)
            df_sorted = df.sort_values(
                by=['交易对方', self.target_column, '交易时间'], 
                ascending=[True, False, False]
            )
            
            self.raw_data = df_sorted
            return df_sorted
        except Exception as e:
            raise Exception(f"数据引擎处理失败: {e}")
    def process_wechat_bill(self, file_path):
        """读取并处理微信账单"""
        try:
            # 1. 读取原始数据
            df = pd.read_excel(file_path, skiprows=17)
            
            # 2. 预清洗：确保金额是数字类型
            # 这一步非常重要，解决了你之前提到的排序不正常问题
            df[self.target_column] = pd.to_numeric(
                df[self.target_column].astype(str).str.replace('¥', ''), 
                errors='coerce'
            )
            
            # 3. 筛选需要的列
            keep_columns = ['交易时间', '交易对方', '商品', '收/支', self.target_column]
            df = df[keep_columns].dropna(subset=[self.target_column])

            # 4. 执行多级排序：商家(A-Z) -> 金额(大到小) -> 时间(新到旧)
            df_sorted = df.sort_values(
                by=['交易对方', self.target_column, '交易时间'], 
                ascending=[True, False, False]
            )
            
            self.raw_data = df_sorted
            return df_sorted
        except Exception as e:
            raise Exception(f"数据引擎处理失败: {e}")

    def get_summary(self):
        """获取简单的收支统计数据"""
        if self.raw_data is None:
            return None
        
        expense = self.raw_data[self.raw_data['收/支'] == '支出'][self.target_column].sum()
        income = self.raw_data[self.raw_data['收/支'] == '收入'][self.target_column].sum()
        return {"支出": expense, "收入": income}