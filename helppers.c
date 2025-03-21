
unsigned char port_byte_in(unsigned short port)
{
    unsigned char result;
    __asm__("in %%dx, %%al" : "=a" (result) : "d" (port));
    return result;
}
void port_byte_out(unsigned short port,unsigned char data)
{
    __asm__("out %%al, %%dx" : : "a" (data), "d" (port));
}
void memory_copy(char *start,char *dest, int amount)
{
    for (int i=0;i<amount;i++)
    {
        dest[i]=start[i];
    }
}
