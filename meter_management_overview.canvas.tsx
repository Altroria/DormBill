import React from 'react';

export default function MeterManagementOverview() {
  return (
    <div style={{ 
      fontFamily: 'Inter, -apple-system, sans-serif',
      background: '#0F172A',
      color: '#F8FAFC',
      minHeight: '100vh',
      padding: '40px 20px'
    }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto' }}>
        {/* Header */}
        <header style={{ marginBottom: '48px' }}>
          <h1 style={{ 
            fontSize: '32px', 
            fontWeight: '700', 
            marginBottom: '12px',
            color: '#F8FAFC'
          }}>
            电表管理功能概览
          </h1>
          <p style={{ fontSize: '16px', color: '#94A3B8', lineHeight: '1.6' }}>
            宿舍电费管理系统 - 总表与空调表分离架构，支持公共用电自动计算与个人分摊
          </p>
        </header>

        {/* Architecture Overview */}
        <section style={{ marginBottom: '40px' }}>
          <div style={{
            background: '#1E293B',
            border: '1px solid #334155',
            borderRadius: '12px',
            padding: '32px',
            marginBottom: '24px'
          }}>
            <h2 style={{ 
              fontSize: '20px', 
              fontWeight: '600', 
              marginBottom: '20px',
              color: '#38BDF8'
            }}>
              🏗️ 系统架构
            </h2>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '24px' }}>
              <div style={{ 
                background: '#0B0E14', 
                border: '1px solid #22D3EE',
                borderRadius: '8px', 
                padding: '20px' 
              }}>
                <h3 style={{ color: '#22D3EE', fontSize: '16px', marginBottom: '12px', fontWeight: '600' }}>
                  数据模型
                </h3>
                <div style={{ fontSize: '14px', lineHeight: '1.8', color: '#CBD5E1' }}>
                  <div style={{ marginBottom: '8px' }}>
                    <code style={{ background: '#1E293B', padding: '2px 6px', borderRadius: '4px', color: '#F97316' }}>
                      RoomMainMeterRecord
                    </code>
                    <span style={{ color: '#64748B' }}> - 房号总表</span>
                  </div>
                  <div style={{ marginBottom: '8px' }}>
                    <code style={{ background: '#1E293B', padding: '2px 6px', borderRadius: '4px', color: '#F97316' }}>
                      MeterRecord
                    </code>
                    <span style={{ color: '#64748B' }}> - 套间空调表</span>
                  </div>
                  <div style={{ fontSize: '12px', color: '#64748B', marginTop: '12px', paddingTop: '12px', borderTop: '1px solid #334155' }}>
                    每个房号一个总表，每个套间一个空调表
                  </div>
                </div>
              </div>

              <div style={{ 
                background: '#0B0E14', 
                border: '1px solid #4FD1C5',
                borderRadius: '8px', 
                padding: '20px' 
              }}>
                <h3 style={{ color: '#4FD1C5', fontSize: '16px', marginBottom: '12px', fontWeight: '600' }}>
                  核心计算逻辑
                </h3>
                <div style={{ fontSize: '14px', lineHeight: '1.8', color: '#CBD5E1' }}>
                  <div style={{ marginBottom: '8px' }}>
                    公共用电 = 总表 - Σ空调表
                  </div>
                  <div style={{ marginBottom: '8px' }}>
                    公共电费 ÷ 房号总人数
                  </div>
                  <div style={{ marginBottom: '8px' }}>
                    空调费 ÷ 套间人数
                  </div>
                  <div style={{ fontSize: '12px', color: '#64748B', marginTop: '12px', paddingTop: '12px', borderTop: '1px solid #334155' }}>
                    个人总电费 = 公共分摊 + 空调分摊
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Backend Components */}
        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ 
            fontSize: '20px', 
            fontWeight: '600', 
            marginBottom: '20px',
            color: '#F8FAFC'
          }}>
            📦 后端组件
          </h2>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px', marginBottom: '24px' }}>
            {[
              { title: 'Models', file: 'meter.py', desc: '电表记录ORM模型', path: 'backend/app/models/' },
              { title: '', file: 'room_main_meter.py', desc: '房号总表模型', path: 'backend/app/models/' },
              { title: 'Routers', file: 'meters.py', desc: 'V1旧版API（已废弃）', path: 'backend/app/routers/' },
              { title: '', file: 'meters_v2.py', desc: 'V2新版API（推荐）', path: 'backend/app/routers/' },
              { title: 'Services', file: 'meter_service.py', desc: '基础电表服务', path: 'backend/app/services/' },
              { title: '', file: 'meter_v2_service.py', desc: 'V2电表服务', path: 'backend/app/services/' },
              { title: '', file: 'electricity_calculation_service.py', desc: '电费计算服务', path: 'backend/app/services/' },
              { title: '', file: 'electricity_service.py', desc: '电费分摊服务', path: 'backend/app/services/' },
              { title: 'Schemas', file: 'meter.py', desc: 'V1数据模型', path: 'backend/app/schemas/' },
              { title: '', file: 'meter_v2.py', desc: 'V2数据模型', path: 'backend/app/schemas/' },
            ].map((item, idx) => (
              <div key={idx} style={{
                background: '#1E293B',
                border: '1px solid #334155',
                borderRadius: '8px',
                padding: '16px'
              }}>
                {item.title && (
                  <div style={{ 
                    fontSize: '12px', 
                    color: '#F59E0B', 
                    fontWeight: '600',
                    marginBottom: '8px' 
                  }}>
                    {item.title}
                  </div>
                )}
                <code style={{ 
                  display: 'block',
                  fontSize: '13px', 
                  color: '#38BDF8',
                  marginBottom: '8px',
                  wordBreak: 'break-word'
                }}>
                  {item.file}
                </code>
                <div style={{ fontSize: '12px', color: '#94A3B8', marginBottom: '4px' }}>
                  {item.desc}
                </div>
                <div style={{ fontSize: '11px', color: '#64748B', fontFamily: 'monospace' }}>
                  {item.path}
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* API Endpoints */}
        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ 
            fontSize: '20px', 
            fontWeight: '600', 
            marginBottom: '20px',
            color: '#F8FAFC'
          }}>
            🔌 API 端点（V2版本）
          </h2>

          <div style={{ display: 'grid', gap: '12px' }}>
            {[
              { 
                method: 'POST', 
                path: '/api/meters-v2/init-month', 
                desc: '初始化月度电表记录',
                params: 'month, building_id',
                returns: 'main_meter_count, ac_meter_count'
              },
              { 
                method: 'GET', 
                path: '/api/meters-v2/combined', 
                desc: '获取组合电表列表（总表+空调表）',
                params: 'month, building_id?, room_no?, skip, limit',
                returns: 'items[], total, skip, limit'
              },
              { 
                method: 'PUT', 
                path: '/api/meters-v2/main/{building_id}/{room_no}/{month}', 
                desc: '更新房号总表读数',
                params: 'current_reading, meter_no?, remark?',
                returns: 'main_meter_record'
              },
              { 
                method: 'PUT', 
                path: '/api/meters-v2/ac/{room_id}/{month}', 
                desc: '更新套间空调表读数',
                params: 'ac_current_reading, ac_meter_no?',
                returns: 'ac_meter_record'
              },
              { 
                method: 'PUT', 
                path: '/api/meters-v2/batch-update', 
                desc: '批量更新电表（推荐）',
                params: 'month, updates[]',
                returns: 'main_meters_updated, ac_meters_updated'
              },
              { 
                method: 'POST', 
                path: '/api/meters-v2/calculate', 
                desc: '批量计算电表费用',
                params: 'building_id?, month?',
                returns: 'main_meters_calculated, ac_meters_calculated'
              },
              { 
                method: 'POST', 
                path: '/api/meters-v2/calculate-enhanced', 
                desc: '增强计算（含公共用电+个人分摊）',
                params: 'month, building_id?, calculate_distribution',
                returns: 'main_meters_calculated, distributions_created, total_fee'
              },
              { 
                method: 'GET', 
                path: '/api/meters-v2/list-enhanced', 
                desc: '获取增强电表列表（含统计）',
                params: 'month, building_id?, room_no?, skip, limit',
                returns: 'items[], total'
              },
            ].map((api, idx) => (
              <div key={idx} style={{
                background: '#1E293B',
                border: '1px solid #334155',
                borderRadius: '8px',
                padding: '16px',
                display: 'grid',
                gridTemplateColumns: '80px 1fr',
                gap: '16px'
              }}>
                <div>
                  <span style={{
                    display: 'inline-block',
                    background: api.method === 'GET' ? '#22D3EE' : api.method === 'POST' ? '#4FD1C5' : '#F59E0B',
                    color: '#0B0E14',
                    padding: '4px 8px',
                    borderRadius: '4px',
                    fontSize: '12px',
                    fontWeight: '600'
                  }}>
                    {api.method}
                  </span>
                </div>
                <div>
                  <code style={{ 
                    display: 'block',
                    color: '#38BDF8', 
                    fontSize: '14px', 
                    marginBottom: '8px',
                    fontFamily: 'monospace'
                  }}>
                    {api.path}
                  </code>
                  <div style={{ fontSize: '13px', color: '#CBD5E1', marginBottom: '6px' }}>
                    {api.desc}
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '8px', fontSize: '12px' }}>
                    <div>
                      <span style={{ color: '#64748B' }}>参数: </span>
                      <span style={{ color: '#94A3B8' }}>{api.params}</span>
                    </div>
                    <div>
                      <span style={{ color: '#64748B' }}>返回: </span>
                      <span style={{ color: '#94A3B8' }}>{api.returns}</span>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Frontend Pages */}
        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ 
            fontSize: '20px', 
            fontWeight: '600', 
            marginBottom: '20px',
            color: '#F8FAFC'
          }}>
            🖥️ 前端页面
          </h2>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '16px' }}>
            {[
              {
                name: 'MeterInput.vue',
                route: '/meter-input',
                title: '电表录入',
                features: [
                  '折叠面板布局（按房号）',
                  '总表+空调表批量录入',
                  '实时计算预览',
                  '批量保存减少请求',
                  '变更追踪与提示'
                ]
              },
              {
                name: 'MeterManageV2.vue',
                route: '/meters',
                title: '电表管理',
                features: [
                  '查询与统计',
                  '公共用电展示',
                  '人均费用计算',
                  '状态管理',
                  '分页加载'
                ]
              },
              {
                name: 'MeterManage.vue',
                route: '（已废弃）',
                title: '电表管理V1',
                features: [
                  '旧版界面',
                  '不推荐使用',
                  '保留向后兼容'
                ]
              }
            ].map((page, idx) => (
              <div key={idx} style={{
                background: '#1E293B',
                border: '1px solid #334155',
                borderRadius: '8px',
                padding: '20px',
                opacity: page.route === '（已废弃）' ? 0.5 : 1
              }}>
                <div style={{ marginBottom: '12px' }}>
                  <code style={{ 
                    fontSize: '14px', 
                    color: '#F97316',
                    fontWeight: '600'
                  }}>
                    {page.name}
                  </code>
                </div>
                <h3 style={{ 
                  fontSize: '16px', 
                  color: '#F8FAFC', 
                  marginBottom: '8px',
                  fontWeight: '600'
                }}>
                  {page.title}
                </h3>
                <div style={{ 
                  fontSize: '13px', 
                  color: '#64748B', 
                  marginBottom: '12px',
                  fontFamily: 'monospace'
                }}>
                  路由: {page.route}
                </div>
                <ul style={{ 
                  margin: 0, 
                  padding: '0 0 0 20px',
                  fontSize: '13px',
                  color: '#94A3B8',
                  lineHeight: '1.8'
                }}>
                  {page.features.map((feature, fidx) => (
                    <li key={fidx}>{feature}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </section>

        {/* Calculation Example */}
        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ 
            fontSize: '20px', 
            fontWeight: '600', 
            marginBottom: '20px',
            color: '#F8FAFC'
          }}>
            💡 计算示例
          </h2>

          <div style={{
            background: '#1E293B',
            border: '1px solid #334155',
            borderRadius: '12px',
            padding: '24px'
          }}>
            <h3 style={{ color: '#F59E0B', marginBottom: '16px', fontSize: '16px', fontWeight: '600' }}>
              201房号 - 4套间6人入住
            </h3>

            <div style={{ display: 'grid', gap: '16px' }}>
              {/* Input */}
              <div style={{
                background: '#0B0E14',
                border: '1px solid #22D3EE',
                borderRadius: '8px',
                padding: '16px'
              }}>
                <div style={{ color: '#22D3EE', fontWeight: '600', marginBottom: '12px', fontSize: '14px' }}>
                  输入数据
                </div>
                <div style={{ fontSize: '13px', lineHeight: '1.8', color: '#CBD5E1' }}>
                  <div style={{ marginBottom: '8px' }}>
                    <strong>总表:</strong> 1000度 → 490元
                  </div>
                  <div>
                    <strong>空调表:</strong>
                    <ul style={{ margin: '4px 0 0 20px', padding: 0 }}>
                      <li>201-1: 100度 → 49元 (2人)</li>
                      <li>201-2: 150度 → 73.5元 (1人)</li>
                      <li>201-3: 120度 → 58.8元 (2人)</li>
                      <li>201-4: 80度 → 39.2元 (1人)</li>
                    </ul>
                  </div>
                </div>
              </div>

              {/* Calculation */}
              <div style={{
                background: '#0B0E14',
                border: '1px solid #4FD1C5',
                borderRadius: '8px',
                padding: '16px'
              }}>
                <div style={{ color: '#4FD1C5', fontWeight: '600', marginBottom: '12px', fontSize: '14px' }}>
                  计算过程
                </div>
                <div style={{ fontSize: '13px', lineHeight: '1.8', color: '#CBD5E1', fontFamily: 'monospace' }}>
                  <div>总空调用电 = 100 + 150 + 120 + 80 = <span style={{ color: '#F59E0B' }}>450度</span></div>
                  <div>公共用电 = 1000 - 450 = <span style={{ color: '#F59E0B' }}>550度</span></div>
                  <div>公共电费 = 490 - (49+73.5+58.8+39.2) = <span style={{ color: '#F59E0B' }}>269.5元</span></div>
                  <div>人均公共电费 = 269.5 ÷ 6 = <span style={{ color: '#F59E0B' }}>44.92元/人</span></div>
                </div>
              </div>

              {/* Result */}
              <div style={{
                background: '#0B0E14',
                border: '1px solid #F59E0B',
                borderRadius: '8px',
                padding: '16px'
              }}>
                <div style={{ color: '#F59E0B', fontWeight: '600', marginBottom: '12px', fontSize: '14px' }}>
                  个人分摊结果
                </div>
                <div style={{ fontSize: '13px', lineHeight: '1.8', color: '#CBD5E1' }}>
                  <div>201-1套间 (2人): 44.92 + 24.5 = <strong>69.42元/人</strong></div>
                  <div>201-2套间 (1人): 44.92 + 73.5 = <strong>118.42元/人</strong></div>
                  <div>201-3套间 (2人): 44.92 + 29.4 = <strong>74.32元/人</strong></div>
                  <div>201-4套间 (1人): 44.92 + 39.2 = <strong>84.12元/人</strong></div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Key Features */}
        <section style={{ marginBottom: '40px' }}>
          <h2 style={{ 
            fontSize: '20px', 
            fontWeight: '600', 
            marginBottom: '20px',
            color: '#F8FAFC'
          }}>
            ✨ 核心特性
          </h2>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '16px' }}>
            {[
              { icon: '🔄', title: '自动带出上月读数', desc: '初始化月度时自动填充' },
              { icon: '⚡', title: '实时计算预览', desc: '输入读数后立即显示用量和费用' },
              { icon: '📦', title: '批量保存', desc: '一次性提交多个房号数据' },
              { icon: '🧮', title: '公共用电自动计算', desc: '总表减空调表自动得出' },
              { icon: '👥', title: '按人数智能分摊', desc: '公共费按总人数，空调费按套间人数' },
              { icon: '💰', title: '尾差处理', desc: '确保分摊金额相加等于总金额' },
              { icon: '⚠️', title: '异常检测', desc: '读数倒退自动标记异常' },
              { icon: '🔒', title: '状态管理', desc: 'pending → recorded → calculated' },
              { icon: '📊', title: '增强查询', desc: '含统计信息和人均费用' },
            ].map((feature, idx) => (
              <div key={idx} style={{
                background: '#1E293B',
                border: '1px solid #334155',
                borderRadius: '8px',
                padding: '20px',
                textAlign: 'center'
              }}>
                <div style={{ fontSize: '32px', marginBottom: '12px' }}>
                  {feature.icon}
                </div>
                <h3 style={{ 
                  fontSize: '14px', 
                  color: '#F8FAFC', 
                  marginBottom: '8px',
                  fontWeight: '600'
                }}>
                  {feature.title}
                </h3>
                <p style={{ 
                  fontSize: '12px', 
                  color: '#94A3B8', 
                  margin: 0,
                  lineHeight: '1.6'
                }}>
                  {feature.desc}
                </p>
              </div>
            ))}
          </div>
        </section>

        {/* Workflow */}
        <section>
          <h2 style={{ 
            fontSize: '20px', 
            fontWeight: '600', 
            marginBottom: '20px',
            color: '#F8FAFC'
          }}>
            📝 操作流程
          </h2>

          <div style={{
            background: '#1E293B',
            border: '1px solid #334155',
            borderRadius: '12px',
            padding: '24px'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
              {[
                { step: '1', text: '初始化月度', color: '#22D3EE' },
                { step: '2', text: '录入总表', color: '#4FD1C5' },
                { step: '3', text: '录入空调表', color: '#F59E0B' },
                { step: '4', text: '批量保存', color: '#F97316' },
                { step: '5', text: '增强计算', color: '#38BDF8' },
                { step: '6', text: '生成结算', color: '#22D3EE' },
              ].map((item, idx) => (
                <React.Fragment key={idx}>
                  <div style={{
                    flex: 1,
                    background: '#0B0E14',
                    border: `2px solid ${item.color}`,
                    borderRadius: '8px',
                    padding: '16px',
                    textAlign: 'center'
                  }}>
                    <div style={{
                      width: '32px',
                      height: '32px',
                      background: item.color,
                      color: '#0B0E14',
                      borderRadius: '50%',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      margin: '0 auto 8px',
                      fontWeight: '700',
                      fontSize: '16px'
                    }}>
                      {item.step}
                    </div>
                    <div style={{ 
                      fontSize: '13px', 
                      color: '#CBD5E1',
                      fontWeight: '600'
                    }}>
                      {item.text}
                    </div>
                  </div>
                  {idx < 5 && (
                    <div style={{ 
                      color: '#475569', 
                      fontSize: '20px',
                      fontWeight: '700'
                    }}>
                      →
                    </div>
                  )}
                </React.Fragment>
              ))}
            </div>
          </div>
        </section>

        {/* Footer */}
        <footer style={{ 
          marginTop: '48px', 
          padding: '24px 0',
          borderTop: '1px solid #334155',
          textAlign: 'center',
          color: '#64748B',
          fontSize: '13px'
        }}>
          <p style={{ margin: 0 }}>
            蓉蓉的收租小工具 - 电表管理系统 | 
            <span style={{ color: '#38BDF8' }}> 基于 FastAPI + Vue3 + Element Plus</span>
          </p>
          <p style={{ margin: '8px 0 0 0' }}>
            文档位置: <code style={{ color: '#F97316' }}>docs/V2_REFACTOR_GUIDE.md</code>
          </p>
        </footer>
      </div>
    </div>
  );
}
