import torch
import torch_dipu

x = torch.randn(3,4,5).cuda()
index = torch.arange(0, 3, 1).cuda()

x[index] = 1
assert torch.allclose(x.cpu(), torch.ones_like(x.cpu()))

x[index] = 0
assert torch.allclose(x.cpu(), torch.zeros_like(x.cpu()))


for shape in [(9, 4, 11, 3), (3, 4, 5), (2, 3), (10,)]:
    values = torch.randn(shape)
    input =  torch.randn(shape)
    indices_cpu = []
    indices_device = []
    for i in range(len(shape)):
        indice = torch.randint(0, min(shape), shape)
        indices_cpu.append(indice)
        indices_device.append(indice.cuda())
    y_cpu = torch.index_put(input.clone(), indices_cpu, values, accumulate = True)
    y_device = torch.index_put(input.cuda(), indices_device, values.cuda(), accumulate = True).cpu()
    assert torch.allclose(y_cpu, y_device.cpu(), atol = 1e-3, rtol = 1e-3)

